# VenusBiblio by IGETech

**Canal oficial de downloads e atualizações do VenusBiblio para Windows.**

[![Validar integridade dos Releases](https://github.com/IGETech01/VenusBiblio-Updates/actions/workflows/validar-release.yml/badge.svg)](https://github.com/IGETech01/VenusBiblio-Updates/actions/workflows/validar-release.yml)
[![Sincronizar descrições](https://github.com/IGETech01/VenusBiblio-Updates/actions/workflows/sincronizar-notas.yml/badge.svg)](https://github.com/IGETech01/VenusBiblio-Updates/actions/workflows/sincronizar-notas.yml)

O VenusBiblio organiza e permite ler livros digitais **PDF e EPUB**, além de **mangás e HQs em CBZ**, com recursos offline, preferências de leitura e acesso ao **Workshop Cliente**.

## Download oficial

### [Baixar a última versão estável para Windows](https://github.com/IGETech01/VenusBiblio-Updates/releases/latest)

**Versão atual: [v0.14.1](https://github.com/IGETech01/VenusBiblio-Updates/releases/tag/v0.14.1)**, publicada em **2 de novembro de 2026**.

- [Instalador Windows v0.14.1](https://github.com/IGETech01/VenusBiblio-Updates/releases/download/v0.14.1/VenusBiblio_Setup_0.14.1.exe)
- [Notas e correções da v0.14.1](docs/releases/v0.14.1.md)
- [Página de atualizações](https://igetech01.github.io/VenusBiblio-Updates/)

O instalador é distribuído **apenas para Windows**. Feche o programa e mantenha uma cópia de segurança dos seus dados antes de instalar ou atualizar.

## Como atualizar

| Versão em uso | Procedimento recomendado |
|---|---|
| **v0.14.0 ou v0.14.1** | Abra **Atualizações → Verificar atualizações**. Se houver erro, utilize o instalador oficial |
| **Versões antigas sem atualizador integrado (incluindo a linha v0.12.x)** | **Baixe e execute manualmente a versão estável mais recente.** O botão de atualização pelo GitHub não existe nessas versões |

**Importante:** versões antigas sem atualizador integrado não podem receber novas versões automaticamente. Por isso, seus instaladores foram retirados da distribuição recomendada. Veja o [guia de migração](docs/MIGRACAO_VERSOES_ANTIGAS.md).

## Recursos

- Leitura offline de livros, PDFs, EPUBs, mangás e histórias em quadrinhos.
- Acervo organizado com capas, pesquisa e preferências de leitura.
- **Workshop Cliente** para recursos disponíveis aos leitores.
- Personalização de interface e experiência de leitura.
- Atualizador integrado nas versões compatíveis, com distribuição oficial pelo GitHub.

### Histórico público

- **[v0.14.1](https://github.com/IGETech01/VenusBiblio-Updates/releases/tag/v0.14.1)**: versão estável atual, com melhorias de desempenho, estabilidade e interface.
- **[v0.14.0](https://github.com/IGETech01/VenusBiblio-Updates/releases/tag/v0.14.0)**: versão estável anterior com atualizador GitHub.
- **[v0.13.1](https://github.com/IGETech01/VenusBiblio-Updates/releases/tag/v0.13.1)**: pré-lançamento técnico **sintético**, criado apenas para testes. **Não instalar.**

**Próxima versão pública planejada: v0.15.0.** As compilações intermediárias são internas e **não** são publicadas neste repositório.

## Android

A portabilidade está em estudo e preparação arquitetural. **Não existe APK oficial nem data de lançamento anunciada.** Este repositório não distribui builds Android.

## Integridade e segurança

Cada Release Windows disponibiliza `manifest.json` e `VenusBiblio_Setup_X.Y.Z.exe`. O manifesto é assinado com **Ed25519** e vincula o instalador a tamanho e **SHA-256**. A [validação automatizada](.github/workflows/validar-release.yml) verifica os arquivos publicados. A assinatura de atualização não equivale à assinatura Authenticode do Windows.

As notas oficiais ficam em [docs/releases](docs/releases), e seus textos são sincronizados automaticamente com as descrições dos Releases por [GitHub Actions](.github/workflows/sincronizar-notas.yml). Acesse a [política de versões](docs/RELEASES_E_ATUALIZACOES.md) para mais detalhes.

**Privacidade:** este repositório **não** inclui o código-fonte proprietário do programa, o Workshop Admin privado, chaves Ed25519 privadas, livros, contas ou dados dos usuários.
