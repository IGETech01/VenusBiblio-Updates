# VenusBiblio | Atualizações oficiais IGETech

Este repositório distribui atualizações do **VenusBiblio by IGETech**.

## Estado atual

- **Release estável publicado:** [v0.12.2](https://github.com/IGETech01/VenusBiblio-Updates/releases/tag/v0.12.2).
- **Desenvolvimento local:** v0.13.0 com prévias v0.14.0. Essas prévias ainda **não** são versões estáveis publicadas.
- **Próximo teste:** pré-lançamento sintético v0.13.1 para validar assinatura, download, instalação e reversão. Esse teste **não** é uma atualização funcional do aplicativo.

## Como são entregues as atualizações

- Windows instalado: `manifest.json` + `VenusBiblio_Setup_X.Y.Z.exe`.
- Código-fonte em testes: `manifest-source.json` + `VenusBiblio_Source_X.Y.Z.zip`.
- Os manifestos são assinados com a chave privada Ed25519 da IGETech e permitem verificar integridade por SHA-256.
- **A chave privada nunca deve ser enviada a este repositório.**

## Verificação automatizada

O workflow [Validar integridade dos Releases](.github/workflows/validar-release.yml) usa o verificador [scripts/verificar_assets_release.py](scripts/verificar_assets_release.py) para conferir os assets de Releases publicados. As verificações no GitHub são complementares aos testes do aplicativo no Windows.

Leia [o plano de teste do atualizador](docs/TESTE_ATUALIZADOR_0131.md). Os testes devem usar um projeto descartável; não instale pacotes sintéticos no VenusBiblio principal.

## Segurança e publicação

- Não publique código do **Workshop Admin**, bancos de dados locais, bibliotecas particulares, backups ou credenciais.
- Nunca apresente uma versão sintética como atualização estável.
- Um Release só deve ser marcado como estável após compilação, assinatura e teste funcional do atualizador no Windows.
