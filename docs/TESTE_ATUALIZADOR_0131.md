# Teste de atualização VenusBiblio (0.13.1)

Este documento descreve um **teste planejado**, não um Release publicado.

- Release estável atual: **v0.12.2**.
- Código local em testes: **0.13.0 / 0.14.0-RC2**.
- Teste proposto: pré-lançamento **v0.13.1**, com somente um `app/versao.py` sintético, sem código proprietário nem dados pessoais.
- Os arquivos `manifest-source.json` e `VenusBiblio_Source_0.13.1.zip` devem ser gerados e assinados no Windows com a chave privada Ed25519 original da IGETech. **Nunca publique a chave privada.**
- O pacote deve ser testado em ambiente descartável, com verificação de assinatura, SHA-256, instalação, restauração e preservação dos dados.
- Como o aplicativo consulta `/releases/latest`, um pré-lançamento **não** aparecerá como atualização estável automática. O teste do botão integrado exige um Release estável completo posterior, devidamente validado.

**Não publicar o pacote sintético como versão estável nem aplicá-lo na instalação principal do VenusBiblio.**
