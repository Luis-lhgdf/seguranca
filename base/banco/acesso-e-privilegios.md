# Banco: exposição de rede, usuários e privilégios

> **Revisado em:** 2026-10-07 · **Origem:** conteúdo compilado de fontes públicas (OWASP, ASVS, NIST, CWE, documentação oficial, avisos de CVE e artigos técnicos) — ver [referências](referencias.md). Se a data estiver antiga (> 6 meses) ou o tema envolver versão/CVE, confirme na fonte oficial antes de aplicar.

## 1. Rede

- Banco **nunca** exposto à internet: VPS → `bind-address = 127.0.0.1` (MySQL; também `mysqlx` 33060) / `listen_addresses = 'localhost'` (Postgres); Docker → só rede interna do Compose, **sem** `ports:` publicando 5432/3306/6379.
- Redis idem (sem senha + porta aberta = RCE clássico).
- `skip-name-resolve` no MySQL.
- Verificação: `ssh $VPS 'sudo ss -tlnp'` → 3306/5432/6379/33060 só em `127.0.0.1`/`::1`; de fora, `nc -zv <host> 3306` deve falhar.
- Banco em loopback dispensa TLS no elo app↔banco; banco remoto/gerenciado exige TLS.

## 2. Usuários e privilégios

- `mysql_secure_installation` (sem usuário anônimo, sem db `test`, root sem login remoto).
- **Usuário da aplicação dedicado**, restrito ao schema e ao host (`app@127.0.0.1`).
- Separar **DML** (aplicação: SELECT/INSERT/UPDATE/DELETE) de **DDL** (migração: CREATE/ALTER/DROP) — `GRANT ALL` no schema, mesmo restrito ao schema, não é menor privilégio. *(Achado típico em auditoria: usuário descrito como "least-privilege" tinha `ALL PRIVILEGES` no schema.)*
- O usuário da app sem `PROCESS` → `mysqldump` precisa de `--no-tablespaces`.
- Usuário de backup só com leitura.
- Verificação: `ssh $VPS "sudo mysql -e \"SHOW GRANTS FOR 'app'@'127.0.0.1'\""` (ou `\du`/`\dp` no Postgres).

## 3. Banco gerenciado na nuvem (se usar)

- Acesso só por rede privada/VPC ou allowlist de IP estrita; TLS obrigatório.
- Credenciais por aplicação, com rotação; IAM/MFA na console do provedor.
- Backups automáticos e PITR ligados; snapshot não público.
- Logs de auditoria do provedor ligados.

## 4. Resiliência de conexão

Dependência exercitada só em **reconexão** (driver, TLS, auth — ex.: `caching_sha2_password` do
MySQL 8 exige `cryptography` no `asyncmy`) não aparece em teste de caminho feliz. *Incidente típico:
API 2h40 com 500 após o `unattended-upgrades` reiniciar o MySQL.* Smoke test de restart
em [infra-vps/operacao-continua.md](../infra-vps/operacao-continua.md#2-smoke-test-de-resiliência).
