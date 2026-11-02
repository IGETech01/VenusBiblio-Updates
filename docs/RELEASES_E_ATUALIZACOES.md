# Downloads e atualizações do VenusBiblio

Este repositório hospeda os **instaladores oficiais para Windows** e informações de atualização do VenusBiblio by IGETech.

## Versão atual

Acesse sempre o endereço permanente:

**[Baixar a versão estável mais recente](https://github.com/IGETech01/VenusBiblio-Updates/releases/latest)**

| Versão | Disponibilidade |
|---|---|
| [v0.14.1](https://github.com/IGETech01/VenusBiblio-Updates/releases/tag/v0.14.1) | Estável atual para Windows |
| [v0.14.0](https://github.com/IGETech01/VenusBiblio-Updates/releases/tag/v0.14.0) | Versão estável anterior |

Versões antigas sem atualização integrada, como a linha v0.12.x, devem ser atualizadas manualmente.

## Como atualizar

1. Faça um backup dos seus livros e configurações.
2. Feche o VenusBiblio.
3. Se o seu aplicativo oferecer **Atualizações → Verificar atualizações**, tente essa opção.
4. Caso não exista o recurso ou a atualização falhe, utilize o instalador oficial da [última versão estável](https://github.com/IGETech01/VenusBiblio-Updates/releases/latest).
5. Abra o programa e confira os dados.

Veja também o [guia para versões antigas](MIGRACAO_VERSOES_ANTIGAS.md).

## Verificação de integridade

As versões para Windows são distribuídas com instalador `VenusBiblio_Setup_X.Y.Z.exe` e arquivo `manifest.json`.

O manifesto é assinado com **Ed25519**, e o processo público de [validação de integridade](../.github/workflows/validar-release.yml) confere a assinatura, o tamanho e o SHA-256 do instalador. A assinatura do manifesto não equivale a uma assinatura Authenticode do Windows.

**Android:** não há APK oficial disponível.
