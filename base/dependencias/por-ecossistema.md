# Auditoria de dependências por ecossistema (comandos)

> **Revisado em:** 2026-10-07. Flags e saídas mudam entre versões das ferramentas: confira `--help` e a documentação oficial antes de usar.

Todos os comandos abaixo são **de leitura** (não alteram lockfile). Rodar na cópia local do
repositório. Comandos que **alteram** (`npm audit fix`, `uv lock --upgrade`, `apt upgrade`) só
com autorização e em branch própria.

## 1. Node / npm (e pnpm/yarn)

```bash
npm ci --ignore-scripts            # instala exatamente o lockfile, sem rodar scripts de pacote
npm audit --audit-level=high       # CVEs conhecidas (sai ≠ 0 se high/critical)
npm audit --omit=dev               # só o que vai para produção
npm outdated                       # atual × desejada × latest
npm ls <pacote>                    # quem puxa uma transitiva
```
pnpm: `pnpm audit`, `pnpm outdated`. yarn: `yarn npm audit`. Correção de transitiva: `overrides`
(npm) / `resolutions` (yarn) com comentário do motivo.

## 2. Python (uv, pip, poetry)

```bash
uv export --frozen --no-dev --format requirements-txt > /tmp/req.txt && pip-audit -r /tmp/req.txt
pip-audit                          # no ambiente ativo
uv pip list --outdated             # ou: pip list --outdated
uv tree                            # árvore de dependências
```
Poetry: `poetry export -f requirements.txt | pip-audit -r /dev/stdin`, `poetry show --outdated`.
SAST de brinde: Ruff com regras `S` (flake8-bandit) ou `bandit -r <pacote>`.

## 3. Pacotes do sistema (Ubuntu/Debian)

```bash
ssh $VPS 'apt list --upgradable 2>/dev/null'
ssh $VPS 'sudo unattended-upgrade --dry-run -d 2>/dev/null | tail -20'
ssh $VPS 'ls /var/run/reboot-required* 2>/dev/null; cat /var/run/reboot-required.pkgs 2>/dev/null'
ssh $VPS 'dpkg -l nginx mysql-server openssh-server openssl | tail -4'
```
CVE por pacote: https://ubuntu.com/security/cves (buscar pelo nome e conferir a versão corrigida
para a release do SO). `pro security-status` mostra o que só o Ubuntu Pro corrige.

## 4. Docker / imagens

```bash
grep -rn "^FROM" $REPO --include=Dockerfile*       # imagens base e tags
docker images --digests
trivy image <imagem:tag>        # ou: docker scout cves <imagem:tag> · grype <imagem:tag>
```
Preferir tag específica (e digest) a `latest`; reconstruir periodicamente para pegar patches da base.

## 5. GitHub Actions

Listar `uses:`; preferir versão fixa (idealmente SHA) de actions de terceiros; Dependabot
`package-ecosystem: github-actions`.

## 6. Serviços

- Nginx: `nginx -v` × https://nginx.org/en/security_advisories.html
- MySQL/Postgres/Redis: versão × notas de release e EOL (endoflife.date).
- OpenSSH/OpenSSL: via USN do SO.
