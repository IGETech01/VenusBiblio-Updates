# Resultado do teste do atualizador VenusBiblio v0.13.1

**Teste executado e aprovado em 2 de novembro de 2026.** A versão v0.13.1 está publicada como **pré-lançamento exclusivamente técnico**, não como aplicativo completo.

## Escopo

O Release contém somente:

- `manifest-source.json`, assinado com a chave Ed25519 de atualização.
- `VenusBiblio_Source_0.13.1.zip`, com um `app/versao.py` sintético.

## Resultados efetivamente obtidos

1. Download real dos dois arquivos do Release pelo GitHub, com hashes correspondentes.
2. Verificação de assinatura Ed25519, tamanho e SHA-256.
3. Rejeição de manifesto adulterado.
4. Aplicação isolada em projeto temporário com dados preservados.
5. Reversão para a versão anterior, sem alterar dados.

**Resultado: 5/5 aprovados.**

O teste **não** exercita o botão da interface nem a consulta `/releases/latest`. Essa rota exclui pré-lançamentos. As versões estáveis Windows posteriores possuem instalador e manifesto assinados, mas seus fluxos de atualização pela interface exigem validação funcional própria.

Consulte as [notas do pré-lançamento](releases/v0.13.1.md) e a [versão estável atual](https://github.com/IGETech01/VenusBiblio-Updates/releases/latest).

**Nunca instalar o pacote sintético na biblioteca principal. Nunca publicar a chave privada.**
