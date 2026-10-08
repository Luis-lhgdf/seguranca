# Segredos e configuração

> **Revisado em:** 2026-10-07 · **Origem:** conteúdo compilado de fontes públicas (OWASP, ASVS, NIST, CWE, documentação oficial, avisos de CVE e artigos técnicos) — ver [referências](referencias.md).

**Cobre:** segredos fora do git e do bundle, validação fail-closed na subida, segredos por
ambiente, `.env` no servidor, rotação, CI/CD (forced-command), Docker `secrets:`.
**Aplica-se quando:** sempre (todo projeto tem ao menos uma credencial).

| Arquivo | Conteúdo |
|---|---|
| [repositorio-e-ambiente.md](repositorio-e-ambiente.md) | git/histórico, bundle, validação, ambientes, servidor, CI |
| [container.md](container.md) | `docker inspect`, `secrets:`, precedência do pydantic-settings |
| [referencias.md](referencias.md) | fontes oficiais e mapeamento Top 10 / ASVS / WSTG |
| [checklist.md](checklist.md) | itens `SEC-SEG-*` (com nível ASVS e mapeamento) |

⚠️ O agente **nunca** lê o conteúdo de `.env`, chaves ou segredos — verifica presença, permissão e
nome de variável (ver [`AGENTS.md`](../../AGENTS.md)).
