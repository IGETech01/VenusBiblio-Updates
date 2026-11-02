"""Valida prerelease GitHub v0.13.1 em ambiente temporario descartavel.

Este teste NAO instala no projeto principal. NAO exercita a GUI nem
/releases/latest: GitHub exclui prereleases desse endpoint por projeto.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

REPO = "IGETech01/VenusBiblio-Updates"
TAG = "v0.13.1"
NOMES = ("manifest-source.json", "VenusBiblio_Source_0.13.1.zip")


def encontrar_gh(especificado: str | None) -> str:
    caminho = shutil.which(especificado or "gh")
    if caminho:
        return caminho
    if especificado and Path(especificado).is_file():
        return str(Path(especificado))
    locais = [
        Path(os.environ.get("ProgramFiles", "C:/Program Files")) / "GitHub CLI" / "gh.exe",
        Path(os.environ.get("LOCALAPPDATA", "")) / "Programs" / "GitHub CLI" / "gh.exe",
        Path(os.environ.get("LOCALAPPDATA", "")) / "Microsoft" / "WinGet" / "Links" / "gh.exe",
    ]
    for local in locais:
        if local.is_file():
            return str(local)
    raise RuntimeError("gh.exe nao localizado. Informe o caminho completo com --gh.")


def executar(*argumentos: str) -> str:
    resultado = subprocess.run(list(argumentos), check=True, capture_output=True, text=True,
                               encoding="utf-8", errors="replace")
    return resultado.stdout.strip()


def verificar_teste(projeto: Path, gh: str) -> None:
    projeto = projeto.resolve()
    if not (projeto / "atualizador_core.py").is_file():
        raise FileNotFoundError("atualizador_core.py ausente na pasta do projeto.")
    sys.path.insert(0, str(projeto))
    import atualizador_core as core

    executar(gh, "auth", "status")
    raw = executar(gh, "release", "view", TAG, "--repo", REPO,
                   "--json", "tagName,isPrerelease,isDraft,assets")
    meta = json.loads(raw)
    if meta.get("tagName") != TAG or meta.get("isDraft") or not meta.get("isPrerelease"):
        raise RuntimeError("O Release de teste nao e um prerelease publicado.")
    registros = {a.get("name"): a for a in meta.get("assets", [])}
    if not all(nome in registros for nome in NOMES):
        raise RuntimeError("Falta um dos dois arquivos no Release de teste.")

    with tempfile.TemporaryDirectory(prefix="venusbiblio_teste_git_") as temp:
        base = Path(temp)
        assets = base / "assets"
        assets.mkdir()

        baixar = [gh, "release", "download", TAG, "--repo", REPO, "--dir", str(assets)]
        for nome in NOMES:
            baixar.extend(("--pattern", nome))
        executar(*baixar)

        for nome in NOMES:
            arquivo = assets / nome
            if not arquivo.is_file():
                raise RuntimeError(f"Arquivo {nome} nao foi baixado.")
            info = registros[nome]
            if arquivo.stat().st_size != info["size"]:
                raise RuntimeError(f"Tamanho inesperado no GitHub: {nome}")
            digest = info.get("digest")
            if digest and digest.startswith("sha256:"):
                atual = hashlib.sha256(arquivo.read_bytes()).hexdigest()
                if atual != digest.removeprefix("sha256:"):
                    raise RuntimeError(f"SHA-256 do GitHub nao confere: {nome}")
        print("OK 1/5: downloads reais do prerelease e hashes da API GitHub.")

        manifesto = assets / NOMES[0]
        zip_fonte = assets / NOMES[1]
        lancamento = core.verificar_manifesto(
            manifesto.read_bytes(), str(manifesto), "0.13.0"
        )
        if lancamento.versao != "0.13.1":
            raise RuntimeError("Versao inesperada no manifesto assinado.")
        itens = core.verificar_pacote(zip_fonte, lancamento)
        if itens != ["versao.py"]:
            raise RuntimeError(f"Pacote sintetico diferente do esperado: {itens}")
        print("OK 2/5: assinatura Ed25519, SHA-256, tamanho e caminho seguro do ZIP.")

        # Confirmar que adulteracoes nao sao aceitas.
        falso = json.loads(manifesto.read_text(encoding="utf-8"))
        falso["payload"]["notas"] = "ADULTERADO"
        try:
            core.verificar_manifesto(json.dumps(falso).encode("utf-8"),
                                     str(manifesto), "0.13.0")
        except core.ErroAtualizacao:
            pass
        else:
            raise AssertionError("Falha critica: manifesto adulterado foi aceito.")
        print("OK 3/5: manifesto adulterado rejeitado.")

        # A raiz real do aplicativo jamais e usada para aplicar/restaurar.
        descartavel = base / "projeto_descartavel"
        descartavel.mkdir()
        arquivo_versao = descartavel / "versao.py"
        arquivo_versao.write_text('VERSAO = "0.13.0"\n', encoding="utf-8")
        dados = descartavel / "dados" / "contas.db"
        dados.parent.mkdir()
        sentinela = b"dados-de-teste-descartaveis"
        dados.write_bytes(sentinela)

        # Este ensaio usa os assets baixados via gh e caminho local assinado.
        # NAO valida a rota /releases/latest do atualizador integrado.
        pendente = core.preparar(lancamento, descartavel)
        resultado = core.aplicar(descartavel, pendente, "0.13.0")
        if resultado.get("versao") != "0.13.1" or 'VERSAO = "0.13.1"' not in arquivo_versao.read_text(encoding="utf-8"):
            raise AssertionError("A versao 0.13.1 nao foi aplicada corretamente.")
        if dados.read_bytes() != sentinela:
            raise AssertionError("A atualizacao alterou os dados de teste.")
        print("OK 4/5: instalacao isolada, com dados preservados.")

        retorno = core.restaurar(descartavel)
        if retorno.get("versao") != "0.13.0" or arquivo_versao.read_text(encoding="utf-8") != 'VERSAO = "0.13.0"\n':
            raise AssertionError("Rollback nao restaurou o arquivo original.")
        if dados.read_bytes() != sentinela:
            raise AssertionError("Rollback alterou dados de teste.")
        print("OK 5/5: rollback restaurou a versao anterior e preservou dados.")
        print("TESTE APROVADO: GitHub + assinatura + instalacao e reversao locais.")
        print("NAO TESTADO: botao de atualizar da GUI e caminho /releases/latest.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--projeto", default=str(Path.cwd()))
    parser.add_argument("--gh", help="Caminho absoluto para gh.exe, caso necessario")
    args = parser.parse_args()
    verificar_teste(Path(args.projeto), encontrar_gh(args.gh))


if __name__ == "__main__":
    try:
        main()
    except (OSError, subprocess.CalledProcessError) as erro:
        print("ERRO NO TESTE:", erro, file=sys.stderr)
        sys.exit(1)
