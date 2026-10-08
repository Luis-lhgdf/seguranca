# Cópias de segurança (backup) e recuperação

> **Revisado em:** 2026-10-07 · **Origem:** conteúdo compilado de fontes públicas (OWASP, ASVS, NIST, CWE, documentação oficial, avisos de CVE e artigos técnicos) — ver [referências](referencias.md).

**Cobre:** o que entra no backup, cifra assimétrica (GPG, servidor sem chave privada), off-site,
pepper separado, retenção × LGPD, teste de restauração, descarte de mídia.
**Aplica-se quando:** há dado persistente sob sua responsabilidade. Em banco gerenciado, ver
também [banco](../banco/acesso-e-privilegios.md#3-banco-gerenciado-na-nuvem-se-usar).

| Arquivo | Conteúdo |
|---|---|
| [estrategia.md](estrategia.md) | regras e decisões de referência |
| [referencias.md](referencias.md) | fontes oficiais |
| [checklist.md](checklist.md) | itens `SEC-BKP-*` |

> Nota: a pasta não se chama `backups/` porque esse nome é bloqueado pelas regras de permissão
> do ambiente do Claude Code nesta máquina.
