# CI, SAST e supply chain

> **Revisado em:** 2026-10-07 · **Origem:** conteúdo compilado de fontes públicas (OWASP, ASVS, NIST, CWE, documentação oficial, avisos de CVE e artigos técnicos) — ver [referências](referencias.md). Se a data estiver antiga (> 6 meses), confirme na fonte oficial.

## 1. Gate antes do deploy

Achado típico em auditoria: o único workflow fazia SSH + script de deploy; **nada** rodava antes — nem
os ~35 testes existentes, nem auditoria; push na `main` ia direto para produção; correções de CVE
eram aplicadas à mão quando o alerta do GitHub chegava.

Job mínimo antes do deploy (bloqueante):
- testes (`pytest`, `vitest`/`jest`), lint, typecheck (`tsc --noEmit`, `mypy`);
- `npm audit --audit-level=high` e `pip-audit`;
- SAST (Ruff `S`/Bandit, Semgrep com regras OWASP);
- secret scanning (gitleaks).

⚠️ Conferir que o `.gitignore` não ignora `.github/` (workflow novo seria descartado em silêncio).

## 2. Atualização contínua

- **Dependabot** (ou Renovate) para npm, pip/uv e github-actions — semanal, minor/patch agrupados, **major em PR isolado** (quebra coisa).
- Piso de versão com motivo comentado onde houve CVE (ex.: `cryptography>=50` por GHSA de PKCS#7).
- Não atualizar às cegas: revisar changelog do que a atualização traz.

## 3. Supply chain

- Lockfile commitado; instalação determinística (`npm ci`, `uv sync --frozen`/`--locked`).
- `--ignore-scripts` onde possível (scripts de instalação executam código do pacote).
- Minimizar dependências no front; SRI em script externo.
- Build em runner descartável, não na VPS de produção (pacote hostil roda com as credenciais do servidor).
- Casos de referência: `event-stream`, `ua-parser-js`, `xz-utils`.
- Template/código de terceiro de origem duvidosa pode vir com backdoor do próprio fornecedor.

## 4. SBOM e prazos

- SBOM (CycloneDX/SPDX: `cyclonedx-py`, `cyclonedx-npm`, `syft`) — ASVS V15.1.2.
- Prazo de remediação por severidade documentado e cumprido — ASVS V15.1.1 (ver [inventario-e-decisao.md](inventario-e-decisao.md#4-prazos-de-remediação-asvs-v1511)).

## 5. DAST

OWASP ZAP contra **staging/local** antes do go-live; contra produção só com autorização (o painel
grava dado real).
