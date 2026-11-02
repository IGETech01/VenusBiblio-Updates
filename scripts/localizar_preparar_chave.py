"""Busca a chave privada ORIGINAL de atualizacoes IGETech e prepara um teste assinado.

Apenas compara chaves publicas derivadas em memoria. Nao envia, nao copia
nem imprime chave privada. O pacote publicado e sintetico (apenas versao.py).
"""
from __future__ import annotations
import argparse
import base64
import hmac
import os
from pathlib import Path
import shutil
import subprocess
import sys
from uuid import uuid4

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

EXCLUIR = {".git", ".venv", "venv", "__pycache__", "build", "dist",
           "node_modules", ".backups", "site-packages", ".pytest_cache"}
EXTENSOES = {".pem", ".key", ".ed25519", ".p8"}

def diretorios_iniciais(preferida: Path, projeto: Path) -> list[Path]:
    home = Path.home()
    candidatos = [preferida,
        home / "OneDrive" / "Documentos" / "IGETECH-Projetos",
        home / "OneDrive" / "Documents" / "IGETECH-Projetos",
        home / "Documents" / "IGETECH-Projetos",
        home / "Documentos" / "IGETECH-Projetos",
        Path("C:/IGETech_Restrito"), home / "Downloads", home / "Documents"]
    resultado = []
    for pasta in candidatos:
        try:
            caminho = pasta.resolve()
            if (not caminho.is_dir() or caminho.is_symlink() or caminho == projeto):
                continue
            if any(caminho == anterior or caminho.is_relative_to(anterior)
                   for anterior in resultado):
                continue
            resultado.append(caminho)
        except OSError:
            pass
    return resultado

def verificar_candidato(path: Path) -> bytes | None:
    try:
        if path.is_symlink() or not 20 <= path.stat().st_size <= 16384:
            return None
        chave = serialization.load_pem_private_key(path.read_bytes(), password=None)
        if not isinstance(chave, Ed25519PrivateKey):
            return None
        return chave.public_key().public_bytes(
            serialization.Encoding.Raw, serialization.PublicFormat.Raw)
    except (ValueError, TypeError, OSError):
        return None

def localizar(pastas: list[Path], pub_atualizador: bytes, pub_admin: bytes):
    encontrada = None
    contagem = {"atualizador": 0, "admin": 0, "outras": 0, "nao_lidas": 0}
    vistas = set()
    for raiz in pastas:
        for atual, diretorios, arquivos in os.walk(raiz, followlinks=False):
            diretorios[:] = [d for d in diretorios
                             if d.lower() not in EXCLUIR and not Path(atual, d).is_symlink()]
            for nome in arquivos:
                caminho = Path(atual) / nome
                if caminho.suffix.lower() not in EXTENSOES:
                    continue
                try:
                    canonico = caminho.resolve()
                    if canonico in vistas or not canonico.is_file():
                        continue
                    vistas.add(canonico)
                    pub = verificar_candidato(caminho)
                except OSError:
                    continue
                if pub is None:
                    contagem["nao_lidas"] += 1
                elif hmac.compare_digest(pub, pub_atualizador):
                    contagem["atualizador"] += 1
                    if encontrada is None:
                        encontrada = caminho
                elif hmac.compare_digest(pub, pub_admin):
                    contagem["admin"] += 1
                else:
                    contagem["outras"] += 1
    return encontrada, contagem

def tentar_publicacao(manifesto: Path, pacote: Path):
    if not shutil.which("gh"):
        print("PUBLICACAO PENDENTE: GitHub CLI nao instalado.")
        return
    if subprocess.run(["gh", "auth", "status"], stdout=subprocess.DEVNULL,
                      stderr=subprocess.DEVNULL).returncode != 0:
        print("PUBLICACAO PENDENTE: execute 'gh auth login'.")
        return
    repo, tag = "IGETech01/VenusBiblio-Updates", "v0.13.1"
    if subprocess.run(["gh", "release", "view", tag, "--repo", repo],
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0:
        print("Release v0.13.1 ja existe. Nao sobrescrevi arquivos.")
        return
    subprocess.run(["gh", "release", "create", tag, str(manifesto), str(pacote),
                    "--repo", repo, "--prerelease", "--latest=false",
                    "--title", "VenusBiblio 0.13.1 | TESTE DO ATUALIZADOR",
                    "--notes", "Teste sintetico. Nao instalar na biblioteca principal."],
                   check=True)
    print("PUBLICADO: prerelease de teste v0.13.1.")

def main():
    args = argparse.ArgumentParser()
    args.add_argument("--projeto", type=Path, required=True)
    args.add_argument("--pasta-inicial", type=Path, required=True)
    args.add_argument("--publicar", action="store_true")
    a = args.parse_args()

    projeto = a.projeto.resolve()
    if not (projeto / "atualizador_core.py").is_file():
        raise FileNotFoundError("Projeto RC2 nao encontrado.")
    sys.path.insert(0, str(projeto))
    import atualizador_core as core
    import permissoes
    from preparar_teste_fonte import preparar

    publica_atualizador = base64.b64decode(core.CHAVE_PUBLICA_B64, validate=True)
    publica_admin = serialization.load_pem_public_key(
        permissoes.PUBLIC_KEY_PEM.encode("ascii")).public_bytes(
            serialization.Encoding.Raw, serialization.PublicFormat.Raw)
    pastas = diretorios_iniciais(a.pasta_inicial, projeto)
    if not pastas:
        raise FileNotFoundError("Nenhuma pasta acessivel para procurar chaves.")
    print("Procurando chaves privadas locais sem revelar seus conteudos...")
    chave, contagem = localizar(pastas, publica_atualizador, publica_admin)
    print("Resultados:", contagem)
    if chave is None:
        print("NAO ENCONTRADA: chave de atualizacoes. A chave Admin nao serve.")
        print("Busque a original 'igetech_ed25519_privada.pem' em backups.")
        return 2

    print("ENCONTRADA: chave de atualizacoes valida e compativel com o VenusBiblio.")
    saida = Path.home() / "AppData" / "Local" / "Temp" / ("VenusBiblio_Teste_" + uuid4().hex)
    manifesto, pacote = preparar(projeto, chave, saida)
    print("PACOTE ASSINADO:", manifesto, pacote, sep="\n")
    print("Chave privada preservada no lugar original; nenhuma copia criada.")
    if a.publicar:
        tentar_publicacao(manifesto, pacote)
    else:
        print("PUBLICACAO PENDENTE: execute novamente com --publicar.")
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as erro:
        print("ERRO:", type(erro).__name__, erro, file=sys.stderr)
        sys.exit(1)
