# Banco de dados

> **Revisado em:** 2026-10-07 · **Origem:** conteúdo compilado de fontes públicas (OWASP, ASVS, NIST, CWE, documentação oficial, avisos de CVE e artigos técnicos) — ver [referências](referencias.md).

**Cobre:** SQL injection, ordenação dinâmica, concorrência/TOCTOU, idempotência, tipos (dinheiro,
null byte), unicidade no banco, RLS (Supabase), exposição de rede, usuários e privilégios, banco
gerenciado, resiliência de conexão.
**Aplica-se quando:** há banco. Itens de banco gerenciado só se usar um; RLS só se o front acessa o banco direto.

| Arquivo | Conteúdo |
|---|---|
| [consultas-e-transacoes.md](consultas-e-transacoes.md) | SQLi, TOCTOU, idempotência, tipos |
| [acesso-e-privilegios.md](acesso-e-privilegios.md) | rede, GRANTs, nuvem, reconexão |
| [referencias.md](referencias.md) | fontes oficiais e mapeamento Top 10 / ASVS / WSTG |
| [checklist.md](checklist.md) | itens `SEC-BD-*` (com nível ASVS e mapeamento) |

Backup: [copias-de-seguranca](../copias-de-seguranca/README.md). Dado sensível/retenção: [privacidade](../privacidade/README.md).
