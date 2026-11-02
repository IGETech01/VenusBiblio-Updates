"""Verificador público de integridade dos assets de Releases VenusBiblio.

Não usa a chave privada, não executa instaladores e não instala atualizações.
"""
from __future__ import annotations
import argparse
import base64
import hashlib
import json
from pathlib import Path
import re
import stat
import zipfile

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

CHAVE_PUBLICA_B64 = "d81atDLW4wz+loTrzvUDPnV+WiTZ2yT/8znTDnKmo0Q="
APP_ID = "IGETech-BibliotecaOffline"
RE_VERSAO = re.compile(r"^v(\d+\.\d+\.\d+)$")


def verificar(manifesto: Path, versao: str) -> None:
    bruto = manifesto.read_bytes()
    if len(bruto) > 65536:
        raise ValueError("Manifesto demasiado grande")
    dados = json.loads(bruto)
    payload = dados["payload"]
    assinatura = base64.b64decode(dados["assinatura"], validate=True)
    if not isinstance(payload, dict) or len(assinatura) != 64:
        raise ValueError("Manifesto ou assinatura inválidos")
    texto = json.dumps(payload, sort_keys=True, separators=(",", ":"),
                       ensure_ascii=False, allow_nan=False).encode("utf-8")
    chave = Ed25519PublicKey.from_public_bytes(base64.b64decode(CHAVE_PUBLICA_B64))
    chave.verify(assinatura, texto)
    if payload.get("aplicativo") != APP_ID or payload.get("versao") != versao:
        raise ValueError("App ou versão não corresponde ao Release")
    arquivo = payload.get("arquivo")
    if not isinstance(arquivo, str) or not re.fullmatch(r"[A-Za-z0-9_][A-Za-z0-9_.-]{0,160}", arquivo):
        raise ValueError("Nome de asset inválido")
    caminho = manifesto.parent / arquivo
    if caminho.is_symlink() or not caminho.is_file():
        raise ValueError("Asset ausente")
    limite = 160 * 1024 * 1024 if manifesto.name == "manifest-source.json" else 768 * 1024 * 1024
    tamanho = caminho.stat().st_size
    if not (1 <= tamanho <= limite) or type(payload.get("tamanho")) is not int or tamanho != payload["tamanho"]:
        raise ValueError("Tamanho diverge do manifesto")
    hash_atual = hashlib.sha256()
    with caminho.open("rb") as handle:
        for bloco in iter(lambda: handle.read(1024 * 1024), b""):
            hash_atual.update(bloco)
    if hash_atual.hexdigest() != payload.get("sha256"):
        raise ValueError("Hash diverge do manifesto")
    if manifesto.name == "manifest-source.json":
        if arquivo != f"VenusBiblio_Source_{versao}.zip":
            raise ValueError("Nome do pacote fonte inesperado")
        with zipfile.ZipFile(caminho) as pacote:
            itens = pacote.infolist()
            if not 1 <= len(itens) <= 160:
                raise ValueError("Quantidade de arquivos inesperada")
            vistos = set()
            for item in itens:
                partes = item.filename.split("/")
                if (len(partes) != 2 or partes[0] != "app"
                    or not re.fullmatch(r"[A-Za-z0-9_][A-Za-z0-9_.-]{0,110}", partes[1])
                    or ".." in partes[1] or item.is_dir()
                    or ((item.external_attr >> 16) & 0o170000) == stat.S_IFLNK):
                    raise ValueError("Entrada insegura no ZIP")
                chave_nome = partes[1].casefold()
                if chave_nome in vistos:
                    raise ValueError("Arquivo duplicado no ZIP")
                vistos.add(chave_nome)
            if "versao.py" not in vistos:
                raise ValueError("versao.py ausente")
            if f'VERSAO = "{versao}"' not in pacote.read("app/versao.py").decode("utf-8"):
                raise ValueError("Versão do pacote divergente")
    else:
        if arquivo != f"VenusBiblio_Setup_{versao}.exe":
            raise ValueError("Nome do instalador inesperado")
        with caminho.open("rb") as handle:
            cabecalho = handle.read(64)
            if len(cabecalho) < 64 or cabecalho[:2] != b"MZ":
                raise ValueError("Instalador não possui cabeçalho MZ")
            posicao = int.from_bytes(cabecalho[60:64], "little")
            if not 64 <= posicao <= 16 * 1024 * 1024:
                raise ValueError("Offset PE fora do intervalo")
            handle.seek(posicao)
            if handle.read(4) != b"PE\x00\x00":
                raise ValueError("Assinatura PE ausente")
    print(f"OK: {manifesto.name} -> {arquivo} ({tamanho} bytes)")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--tag", required=True)
    p.add_argument("--dir", required=True, type=Path)
    args = p.parse_args()
    match = RE_VERSAO.fullmatch(args.tag)
    if not match:
        raise ValueError("Tag deve ser vMAIOR.MENOR.CORRECAO")
    pasta = args.dir.resolve()
    manifestos = [pasta / n for n in ("manifest.json", "manifest-source.json") if (pasta / n).is_file()]
    if not manifestos:
        raise ValueError("Nenhum manifesto encontrado")
    for manifesto in manifestos:
        verificar(manifesto, match.group(1))
    print("MANIFESTOS E ASSETS VALIDADOS")


if __name__ == "__main__":
    main()
