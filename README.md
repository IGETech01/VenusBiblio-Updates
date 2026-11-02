# VenusBiblio by IGETech | Atualizações oficiais

Canal público de distribuição do **VenusBiblio**, biblioteca digital para Windows com leitura offline de livros, mangás e HQs.

## Versão estável mais recente

**[VenusBiblio v0.14.0](https://github.com/IGETech01/VenusBiblio-Updates/releases/tag/v0.14.0)**, publicada em **2 de novembro de 2026**.

- **Windows:** baixe `VenusBiblio_Setup_0.14.0.exe`.
- **Atualização integrada:** abra **Atualizações → Verificar atualizações** no programa; se o instalador não for oferecido, use o arquivo oficial do Release.
- **Segurança:** o `manifest.json` é assinado com Ed25519 e vincula a versão ao tamanho e SHA-256 do instalador.

### Histórico de versões

| Versão | Tipo | Situação |
|---|---|---|
| **[v0.14.0](https://github.com/IGETech01/VenusBiblio-Updates/releases/tag/v0.14.0)** | Estável Windows | Publicada, instalador completo |
| **[v0.13.1](https://github.com/IGETech01/VenusBiblio-Updates/releases/tag/v0.13.1)** | Pré-lançamento técnico | Teste sintético do atualizador. **Não instalar em produção** |
| **[v0.12.2](https://github.com/IGETech01/VenusBiblio-Updates/releases/tag/v0.12.2)** | Estável anterior | Substituída pela v0.14.0 |
| **v0.14.1** | Desenvolvimento e testes locais | **Ainda não publicada**; desempenho, refinamentos visuais e preparação interna para Android |

Veja o histórico e as notas completas em [docs/releases](docs/releases) e [a política de lançamentos](docs/RELEASES_E_ATUALIZACOES.md).

## Recursos do aplicativo

- Biblioteca de leitura offline: **PDF, EPUB, mangás e HQs em CBZ**.
- Organização de acervo e personalização da leitura.
- **Workshop Cliente** e distribuição de conteúdo disponível.
- Interface escura, detalhes roxos e temas opcionais.
- Sistema de atualização pelo GitHub, com verificação criptográfica e mecanismo de recuperação.

**Android:** há preparação técnica interna em desenvolvimento; **não existe APK oficial publicado**.

## Arquivos e integridade

O Release estável Windows utiliza `manifest.json` e `VenusBiblio_Setup_X.Y.Z.exe`. Pré-lançamentos técnicos podem utilizar `manifest-source.json` e um ZIP sintético, sem serem instaladores do aplicativo.

O workflow [Validar integridade dos Releases](.github/workflows/validar-release.yml) verifica assinatura Ed25519, tamanho e SHA-256. O evento de publicação da v0.14.0 foi validado com sucesso. A assinatura de atualização não é um certificado Authenticode do Windows.

## Descrições sempre sincronizadas

As notas oficiais de cada versão ficam em [docs/releases](docs/releases). O workflow de sincronização e o script [sincronizar_notas_releases.ps1](scripts/sincronizar_notas_releases.ps1) atualizam as **descrições dos Releases**, sem alterar instaladores, tags ou canais.

## Segurança

Este repositório **não** distribui código-fonte privado, chaves de assinatura, dados de usuários, bibliotecas particulares ou ferramentas exclusivas do Workshop Admin. A chave privada de atualização IGETech deve permanecer no computador confiável da editora.
