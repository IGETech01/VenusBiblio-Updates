# Migração de versões antigas do VenusBiblio

A versão pública recomendada do **VenusBiblio by IGETech** é a **[última versão estável](https://github.com/IGETech01/VenusBiblio-Updates/releases/latest)** para Windows.

## Por que algumas versões não atualizam automaticamente?

O atualizador integrado ao GitHub foi introduzido depois das versões iniciais do aplicativo. **A linha v0.12.x não dispõe desse mecanismo**, portanto não consegue obter as versões atuais pelo botão de atualização.

Para evitar instalações obsoletas, a IGETech retirou a distribuição recomendada desses instaladores. **Não utilize arquivos antigos de fontes não oficiais.**

## Atualização manual

1. Faça uma cópia de segurança dos seus livros, contas, dados e configurações. Anote a pasta de armazenamento utilizada pela sua instalação antiga.
2. Feche o VenusBiblio.
3. Acesse a [página de Releases](https://github.com/IGETech01/VenusBiblio-Updates/releases/latest) e baixe o instalador Windows da versão estável mais recente.
4. Execute o instalador oficial por usuário. Se o instalador solicitar confirmação sobre caminhos ou dados existentes, revise antes de continuar.
5. Abra o aplicativo e confirme a versão, os livros, o login, as preferências e a leitura de PDF/EPUB/CBZ.
6. A partir de uma versão compatível, use **Atualizações → Verificar atualizações** para conferir lançamentos posteriores.

**Se os seus dados não aparecerem, não os apague nem desinstale às cegas.** Preserve o backup e confira os caminhos de dados das duas instalações antes de tentar migrar.

## Integridade

Os Releases oficiais do Windows distribuem `manifest.json` e o instalador `VenusBiblio_Setup_X.Y.Z.exe`. O manifesto é assinado digitalmente com Ed25519 para o fluxo de atualização do aplicativo. Essa assinatura não substitui uma assinatura Authenticode do Windows.

**Não existe versão oficial Android publicada.** A próxima versão pública planejada é a **v0.15.0**; os builds de desenvolvimento intermediários são privados.
