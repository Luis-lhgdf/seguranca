# Dependências, versões e atualizações

> **Revisado em:** 2026-10-07 · **Origem:** conteúdo compilado de fontes públicas (OWASP, ASVS, NIST, CWE, documentação oficial, avisos de CVE e artigos técnicos) — ver [referências](referencias.md).

**Cobre:** inventário de versões de todas as camadas, checagem de versão atual/EOL/CVE **na web na
data da auditoria**, decisão de subir ou voltar com justificativa, prazos de remediação, comandos
por ecossistema (npm, Python/uv, apt, Docker, Actions), gate de CI, SAST, supply chain, SBOM.
**Aplica-se quando:** sempre.

| Arquivo | Conteúdo |
|---|---|
| [inventario-e-decisao.md](inventario-e-decisao.md) | o que inventariar, onde checar, matriz de decisão, prazos |
| [por-ecossistema.md](por-ecossistema.md) | comandos de leitura por ecossistema |
| [ci-e-supply-chain.md](ci-e-supply-chain.md) | gate, Dependabot, lockfile, build, SBOM, DAST |
| [referencias.md](referencias.md) | fontes oficiais |
| [checklist.md](checklist.md) | itens `SEC-DEP-*` |

⚠️ Este é o tema que mais envelhece. O agente **não confia** na base nem na própria memória para
dizer qual é a versão atual: pesquisa na fonte oficial e cita link + data.
