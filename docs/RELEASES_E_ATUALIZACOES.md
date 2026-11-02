# Política de versões e descrições do VenusBiblio

Este repositório é o **canal público de atualizações**, não o repositório do código-fonte privado da IGETech.

## Estado verificado em 2/11/2026

| Versão | Canal | Situação |
|---|---|---|
| [v0.14.0](https://github.com/IGETech01/VenusBiblio-Updates/releases/tag/v0.14.0) | Estável Windows | Publicada: `manifest.json` + instalador `.exe` |
| [v0.13.1](https://github.com/IGETech01/VenusBiblio-Updates/releases/tag/v0.13.1) | Pré-lançamento técnico | Teste sintético do atualizador; não instalar |
| [v0.12.2](https://github.com/IGETech01/VenusBiblio-Updates/releases/tag/v0.12.2) | Estável anterior | Instalador Windows publicado |
| v0.14.1 | Desenvolvimento | Patch de desempenho/interface + base técnica Android; **ainda não publicado**; hotfix aguarda validação no Windows |

## Regras obrigatórias para cada lançamento

1. Registrar as mudanças e limitações em `docs/releases/vX.Y.Z.md`.
2. Atualizar o README e, se necessário, a página `index.html`.
3. Testar o instalador e o fluxo de atualização, inclusive preservação de dados.
4. Assinar o manifesto Ed25519 **somente no computador confiável**. Nunca enviar ou versionar a chave privada.
5. Criar o Release como **rascunho** e anexar somente o instalador e os manifestos de distribuição.
6. Validar assinatura, hash SHA-256 e tamanho dos assets baixados do GitHub.
7. Atualizar o texto da **descrição do Release no GitHub** com as notas correspondentes, por meio do `scripts/sincronizar_notas_releases.ps1`.
8. Publicar somente após as verificações. Conferir novamente o estado e a descrição no GitHub.

**Observação:** editar arquivos Markdown no repositório **não** modifica automaticamente as descrições de Releases já publicados. Execute o script de sincronização do passo 7 (com `gh` autenticado) após editar as notas.

## Segurança e limitações

- O Release `v0.13.1` é exclusivamente técnico e não atualiza o aplicativo principal.
- Android está em estudo técnico interno. Não há APK publicado nem data confirmada.
- Não publicar código privado do Workshop Admin, banco de dados, contas, livros de usuários ou credenciais.
- Manifestos devem ser verificados pelo cliente; uma assinatura Ed25519 de atualização não substitui uma assinatura Windows Authenticode.
