"""Baixa assets reais do GitHub e testa assinatura, instalação e reversão.

O teste é executado APENAS numa pasta temporária descartável.
Não modifica a instalação nem os livros do usuário.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

REPO = "IGETech01/VenusBiblio-Updates"
TAG = "v0.13.1"


def testar(projeto: Path) -> None:
    projeto = projeto.resolve()
    if not (projeto / "atualizador_core.py").is_file():
        raise FileNotFoundError("atualizador_core.py ausente na raiz do projeto.")
    sys.path.insert(0, str(projeto))
    import atualizador_core as core

    if not shutil.which("gh"):
        raise RuntimeError("GitHub CLI ausente. Instale gh e use gh auth login.")

    with tempfile.TemporaryDirectory(prefix="venusbiblio_teste_git_") as temp:
        base = Path(temp)
        assets = base / "assets"
        assets.mkdir()
        subprocess.run([
            "gh", "release", "download", TAG, "--repo", REPO,
            "--pattern", "manifest-source.json",
            "--pattern", "VenusBiblio_Source_0.13.1.zip",
            "--dir", str(assets),
        ], check=True)

        manifesto = assets / "manifest-source.json"
        zip_fonte = assets / "VenusBiblio_Source_0.13.1.zip"
        if not manifesto.is_file() or not zip_fonte.is_file():
            raise RuntimeError("Pré-lançamento incompleto no GitHub.")

        lancamento = core.verificar_manifesto(
            manifesto.read_bytes(), str(manifesto), "0.13.0"
        )
        if lancamento.versao != "0.13.1":
            raise RuntimeError("Versão inesperada.")
        itens = core.verificar_pacote(zip_fonte, lancamento)
        if "versao.py" not in itens:
            raise RuntimeError("Pacote não contém versao.py.")

        descartavel = base / "projeto_descartavel"
        descartavel.mkdir()
        (descartavel / "versao.py").write_text('VERSAO = "0.13.0"\n', encoding="utf-8")
        dados = descartavel / "dados" / "contas.db"
        dados.parent.mkdir()
        dados.write_bytes(b"dados-de-teste-descartaveis")

        pendente = core.preparar(lancamento, descartavel)
        resultado = core.aplicar(descartavel, pendente, "0.13.0")
        if resultado.get("versao") != "0.13.1":
            raise RuntimeError("A atualização não foi aplicada.")
        if dados.read_bytes() != b"dados-de-teste-descartaveis":
            raise RuntimeError("O teste modificou dados privados descartáveis.")

        retorno = core.restaurar(descartavel)
        if retorno.get("versao") != "0.13.0":
            raise RuntimeError("A reversão não restaurou a versão anterior.")
        if dados.read_bytes() != b"dados-de-teste-descartaveis":
            raise RuntimeError("A reversão modificou os dados descartáveis.")

        print("TESTE APROVADO: GitHub -> download -> assinatura -> hash -> instalação -> reversão.")
        print(f"Arquivos verificados: {len(itens)}. Biblioteca real: não modificada.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--projeto", default=str(Path.cwd()))
    args = parser.parse_args()
    testar(Path(args.projeto))


if __name__ == "__main__":
    main()
