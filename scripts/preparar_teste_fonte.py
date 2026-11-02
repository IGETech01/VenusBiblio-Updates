"""Prepara um prerelease sintético do VenusBiblio para testar o atualizador.

O ZIP público terá apenas app/versao.py. Não contém bibliotecas,
Workshop Admin, código proprietário ou chaves.
"""
from __future__ import annotations

import argparse
from dataclasses import replace
import hashlib
from pathlib import Path
import shutil
import subprocess
import sys
import zipfile

REPO = "IGETech01/VenusBiblio-Updates"
VERSAO_TESTE = "0.13.1"
BASE_ESPERADA = "0.13.0"


def preparar(projeto: Path, chave: Path, saida: Path) -> tuple[Path, Path]:
    projeto = projeto.resolve()
    chave = chave.resolve()
    saida = saida.resolve()
    if not (projeto / "main.py").is_file() or not (projeto / "versao.py").is_file():
        raise ValueError("Projeto VenusBiblio RC2 não localizado.")
    if saida == projeto or saida.is_relative_to(projeto) or projeto.is_relative_to(saida):
        raise ValueError("A saída precisa ficar fora da pasta principal do projeto.")
    if not chave.is_file():
        raise FileNotFoundError("Arquivo de chave privada não encontrado.")

    sys.path.insert(0, str(projeto))
    import gerar_pacote_fonte_igetech as gerador
    import publicar_fonte_igetech as publicador
    import atualizador_core as core

    if gerador.ler_versao(projeto / "versao.py") != BASE_ESPERADA:
        raise ValueError(f"A base do teste precisa ser {BASE_ESPERADA}.")
    if saida.exists() and any(saida.iterdir()):
        raise FileExistsError("A pasta de saída precisa estar vazia.")
    saida.mkdir(parents=True, exist_ok=True)

    pacote = saida / f"VenusBiblio_Source_{VERSAO_TESTE}.zip"
    codigo = (
        f'VERSAO = "{VERSAO_TESTE}"\n'
        'CANAL = "TESTE ISOLADO"\n'
        f'URL_ATUALIZACOES = "https://github.com/{REPO}"\n'
    )
    with zipfile.ZipFile(pacote, "x", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        z.writestr("app/versao.py", codigo)

    lan = core.Lancamento(
        VERSAO_TESTE, "Teste sintético", pacote.name, "0" * 64,
        pacote.stat().st_size, str(pacote), b""
    )
    lan = replace(lan, sha256=hashlib.sha256(pacote.read_bytes()).hexdigest())
    core.verificar_pacote(pacote, lan)

    assets = saida / "assets"
    publicador.publicar(
        pacote, chave, assets,
        "Teste sintético do atualizador; nenhum arquivo proprietário incluído."
    )
    return assets / "manifest-source.json", assets / pacote.name


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--projeto", default=str(Path.cwd()))
    p.add_argument("--chave", required=True, help="Caminho local da chave privada IGETech")
    p.add_argument("--saida", required=True)
    p.add_argument("--publicar", action="store_true")
    args = p.parse_args()

    manifesto, pacote = preparar(Path(args.projeto), Path(args.chave), Path(args.saida))
    print("Pacote assinado preparado:", manifesto, pacote, sep="\n")
    print("Código privado e projeto original não foram alterados.")

    if args.publicar:
        if not shutil.which("gh"):
            raise RuntimeError("GitHub CLI ausente. Instale o gh e use gh auth login.")
        subprocess.run([
            "gh", "release", "create", f"v{VERSAO_TESTE}", str(manifesto), str(pacote),
            "--repo", REPO, "--prerelease", "--latest=false",
            "--title", f"VenusBiblio {VERSAO_TESTE} | TESTE DO ATUALIZADOR",
            "--notes", "Pré-lançamento sintético de teste. Não instalar em produção."
        ], check=True)
        print("Pré-lançamento publicado. A versão estável não foi substituída.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
