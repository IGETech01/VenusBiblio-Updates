# Política de versões e lançamentos do VenusBiblio

Este repositório é o **canal público de atualizações do VenusBiblio by IGETech**. O código-fonte proprietário, as chaves privadas e os dados de usuários não são distribuídos aqui.

## Canal estável (verificado em 2 de novembro de 2026)

| Versão | Estado | Observações |
|---|---|---|
| [v0.14.1](https://github.com/IGETech01/VenusBiblio-Updates/releases/tag/v0.14.1) | **Última estável Windows** | Instalador + manifesto Ed25519; verificação de integridade aprovada |
| [v0.14.0](https://github.com/IGETech01/VenusBiblio-Updates/releases/tag/v0.14.0) | Estável anterior | Primeiro ciclo estável com atualizador integrado ao GitHub |
| [v0.13.1](https://github.com/IGETech01/VenusBiblio-Updates/releases/tag/v0.13.1) | Pré-lançamento técnico | Pacote sintético de teste. **Não instalar como aplicativo** |
| Linha v0.12.x | **Obsoleta, sem distribuição recomendada** | Não possui atualizador GitHub. Atualize manualmente usando a versão estável mais recente |

**Próximo lançamento público:** v0.15.0. As versões de desenvolvimento 0.14.x-dev posteriores à 0.14.1 são internas e não serão publicadas em Releases.

**Android:** preparação técnica interna; não existe APK oficial nem data anunciada.

## Atualização e migração

- Quem já possui uma instalação com atualizador GitHub pode usar **Atualizações → Verificar atualizações**.
- Quem possui versão sem atualizador integrado precisa baixar manualmente o [instalador mais recente](https://github.com/IGETech01/VenusBiblio-Updates/releases/latest), após fazer backup.
- Leia o [guia de migração de versões antigas](MIGRACAO_VERSOES_ANTIGAS.md).
- O teste funcional completo do botão de atualização da v0.14.0 para v0.14.1 ainda não foi confirmado nesta documentação.

## Procedimento para um lançamento público

1. Compilar e testar o aplicativo Windows, incluindo preservação de dados.
2. Registrar recursos, limitações e resultados em `docs/releases/vX.Y.Z.md`.
3. Assinar o manifesto Ed25519 **no computador confiável**. Nunca publicar a chave privada.
4. Criar um Release como rascunho, com somente os assets de distribuição.
5. Baixar os assets do próprio rascunho e validar assinatura Ed25519, SHA-256, tamanho e formato do instalador.
6. Publicar apenas após aprovação; conferir [a validação automatizada](../.github/workflows/validar-release.yml).
7. Revisar README, página de downloads e notas da versão; confirmar a sincronização das descrições.

A automação [sincronizar-notas.yml](../.github/workflows/sincronizar-notas.yml) atualiza o texto das descrições de Releases **existentes**, usando as notas versionadas. O script [sincronizar_notas_releases.ps1](../scripts/sincronizar_notas_releases.ps1) também pode sincronizá-las manualmente. Essa operação **não** modifica tags ou instaladores e não publica novos Releases.

## Segurança e privacidade

- Não incluir chaves privadas, bibliotecas pessoais, banco de dados, credenciais ou ferramentas privadas do Workshop Admin.
- Não disponibilizar pacotes sintéticos de teste como instaladores.
- A assinatura Ed25519 do atualizador **não é** uma assinatura Authenticode do Windows.
- Versões sem canal de atualização funcional não devem continuar disponíveis como download recomendado.
