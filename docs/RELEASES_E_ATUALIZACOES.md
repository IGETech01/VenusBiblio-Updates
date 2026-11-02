# Política de versões e descrições do VenusBiblio

Este repositório é o **canal público de atualizações**, não o repositório do código-fonte privado da IGETech.

## Estado verificado em 2 de novembro de 2026

| Versão | Canal | Situação |
|---|---|---|
| [v0.14.1](https://github.com/IGETech01/VenusBiblio-Updates/releases/tag/v0.14.1) | **Estável atual (Windows)** | Publicada: manifesto Ed25519 + instalador EXE; workflow de integridade aprovado |
| [v0.14.0](https://github.com/IGETech01/VenusBiblio-Updates/releases/tag/v0.14.0) | Estável anterior | Distribuída com instalador Windows; substituída pela v0.14.1 |
| [v0.13.1](https://github.com/IGETech01/VenusBiblio-Updates/releases/tag/v0.13.1) | Pré-lançamento técnico | Teste sintético do atualizador; **não instalar** |
| [v0.12.2](https://github.com/IGETech01/VenusBiblio-Updates/releases/tag/v0.12.2) | Estável anterior | Instalador Windows antigo |

**Acompanhamento da v0.14.1:** o instalador foi compilado e validado, mas o botão de atualização integrada de uma instalação real v0.14.0 para v0.14.1 ainda precisa ser confirmado.

**Android:** somente preparação arquitetural interna. Não há versão Android, APK nem data de lançamento anunciada.

## Regras de cada lançamento

1. Registrar recursos, limitações e mudanças em `docs/releases/vX.Y.Z.md`.
2. Atualizar o README e a página `index.html` para a versão estável atual.
3. Testar o instalador e, sempre que possível, o fluxo de atualização e a preservação de dados.
4. Assinar o manifesto Ed25519 **somente no computador confiável**. Nunca enviar ou versionar a chave privada.
5. Criar um Release como **rascunho** e anexar apenas assets de distribuição.
6. Validar assinatura, SHA-256 e tamanho dos arquivos baixados do GitHub.
7. Publicar como estável somente após as verificações necessárias.
8. Confirmar os workflows e **as descrições dos Releases** publicados.

## Sincronização automática das descrições

O workflow [sincronizar-notas.yml](../.github/workflows/sincronizar-notas.yml) atualiza os textos dos Releases existentes quando há alteração em `docs/releases/v*.md` na branch `main`. Também é possível executar [sincronizar_notas_releases.ps1](../scripts/sincronizar_notas_releases.ps1) manualmente com o GitHub CLI.

**A automação altera somente as descrições**. Não cria, instala, substitui nem publica executáveis ou Releases e não modifica as tags. Conferir o resultado do workflow após cada alteração.

## Segurança e limitações

- Não anunciar pacotes de teste como versões estáveis, nem publicar conteúdo privado do Workshop Admin.
- Não publicar bancos de dados, livros de usuários, credenciais ou chaves de assinatura.
- A assinatura Ed25519 do atualizador não é uma assinatura Authenticode do Windows.
