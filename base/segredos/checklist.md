# Checklist — Segredos e configuração (SEG)

> **Revisado em:** 2026-10-07. Variáveis e regras em [`AGENTS.md`](../../AGENTS.md). **Nunca** imprimir valor de segredo: só nome, presença e permissão.

### SEC-SEG-01 — Nenhum segredo no histórico do git
- **Aplica-se quando:** sempre.
- **Risco se faltar:** qualquer pessoa com acesso ao repositório (ou se ele ficar público) pega as chaves.
- **Como verificar:** `gitleaks detect --source $REPO --redact` (o `--redact` evita imprimir o valor); `git -C $REPO log --all --diff-filter=A --name-only | grep -E '(^|/)\.env$|\.pem$|\.key$'`.
- **OK quando:** zero achados (ou achados já rotacionados e documentados).
- **Referência:** [repositorio-e-ambiente.md#1-fora-do-git](repositorio-e-ambiente.md#1-fora-do-git) · ASVS V13.
- **Mapeamento:** nível L2 · Top 10 A02:2025, A04:2025 · ASVS V13.3.1 (L2).

### SEC-SEG-02 — `.gitignore` correto e sem regra que esconda o que deve ser versionado
- **Aplica-se quando:** sempre.
- **Risco se faltar:** `.env` commitado por engano; ou workflow de CI descartado em silêncio.
- **Como verificar:** ler `.gitignore`; `git -C $REPO check-ignore -v --no-index .env backend/.env .github/workflows/x.yml`.
- **OK quando:** segredos ignorados, `.env.example` versionado, `.github/workflows` não ignorado.
- **Referência:** [repositorio-e-ambiente.md#1-fora-do-git](repositorio-e-ambiente.md#1-fora-do-git).
- **Mapeamento:** nível L1 · Top 10 A02:2025 · ASVS V13.4.1 (L1) · WSTG-CONF-04.

### SEC-SEG-03 — Nenhum segredo no bundle do front
- **Aplica-se quando:** há front compilado.
- **Risco se faltar:** a chave vai para o navegador de todo visitante.
- **Como verificar:** listar variáveis públicas (`grep -rhoE "NEXT_PUBLIC_[A-Z_]+|VITE_[A-Z_]+" $REPO | sort -u`); varrer o build (grep da seção 2).
- **OK quando:** só valores públicos por desenho.
- **Referência:** [repositorio-e-ambiente.md#2-fora-do-front](repositorio-e-ambiente.md#2-fora-do-front).
- **Mapeamento:** nível L2 · Top 10 A02:2025 · ASVS V13.3.1 (L2) · WSTG-INFO-05.

### SEC-SEG-04 — App recusa subir com segredo fraco ou placeholder
- **Aplica-se quando:** há chave de assinatura, pepper ou credencial em config.
- **Risco se faltar:** produção roda com `TROQUE_ESTE_VALOR`.
- **Como verificar:** ler validadores da config (tamanho mínimo, placeholder, `CORS=*`, chave de teste).
- **OK quando:** validação fail-closed na inicialização.
- **Referência:** [repositorio-e-ambiente.md#3-validação-na-subida-fail-closed](repositorio-e-ambiente.md#3-validação-na-subida-fail-closed).
- **Mapeamento:** nível L2 · Top 10 A02:2025 · ASVS V13.2.3 (L2).

### SEC-SEG-05 — Segredos distintos por ambiente
- **Aplica-se quando:** existe mais de um ambiente (inclusive a máquina do dev).
- **Risco se faltar:** token assinado em dev vale em produção.
- **Como verificar:** perguntar ao responsável como foram gerados; comparar **hashes** (não valores) se ele autorizar: `sha256sum` do valor em cada ambiente.
- **OK quando:** gerados separadamente, no servidor.
- **Referência:** [repositorio-e-ambiente.md#4-por-ambiente](repositorio-e-ambiente.md#4-por-ambiente).
- **Mapeamento:** nível L2 · Top 10 A02:2025 · ASVS V13.3.1 (L2).

### SEC-SEG-06 — `.env` de produção com permissão restrita
- **Aplica-se quando:** há `.env` no servidor.
- **Risco se faltar:** qualquer usuário/processo do servidor lê os segredos.
- **Como verificar:** `ssh $VPS 'stat -c "%a %U:%G %n" <caminho>/.env'` (sem `cat`).
- **OK quando:** `600` ou `640` com grupo da conta de serviço; dono correto.
- **Referência:** [repositorio-e-ambiente.md#5-no-servidor](repositorio-e-ambiente.md#5-no-servidor).
- **Mapeamento:** nível L2 · Top 10 A02:2025 · ASVS V13.3.2 (L2) · WSTG-CONF-09.

### SEC-SEG-07 — Segredos não vazam por `docker inspect`
- **Aplica-se quando:** roda em Docker.
- **Risco se faltar:** quem acessa o daemon lê todas as chaves.
- **Como verificar:** `ssh $VPS 'docker inspect <conteiner> --format "{{range .Config.Env}}{{println .}}{{end}}" | cut -d= -f1'` (só **nomes**) e conferir se nomes de segredo aparecem; ler `compose.yaml` (`secrets:`).
- **OK quando:** nenhum segredo como variável de ambiente (ou risco aceito por escrito).
- **Referência:** [container.md#3-secrets-do-compose-não-precisa-de-swarm](container.md#3-secrets-do-compose-não-precisa-de-swarm).
- **Mapeamento:** nível L2 · Top 10 A02:2025 · ASVS V13.3.1 (L2), V13.3.2 (L2).

### SEC-SEG-08 — Chave de deploy do CI com forced-command
- **Aplica-se quando:** CI faz deploy por SSH.
- **Risco se faltar:** chave vazada do CI = shell no servidor.
- **Como verificar:** `ssh $VPS 'grep -c "command=" ~deploy/.ssh/authorized_keys'` e ler as opções da linha (sem imprimir a chave: `cut -d" " -f1`).
- **OK quando:** `command=` + `no-port-forwarding,no-pty` (ou equivalente).
- **Referência:** [repositorio-e-ambiente.md#6-cicd](repositorio-e-ambiente.md#6-cicd).
- **Mapeamento:** nível L2 · Top 10 A08:2025, A03:2025 · ASVS V13.3.2 (L2).

### SEC-SEG-09 — Rotação de segredos planejada
- **Aplica-se quando:** sempre.
- **Risco se faltar:** segredo vazado continua valendo; ninguém sabe como trocar.
- **Como verificar:** procurar procedimento escrito por segredo (JWT, pepper, banco, gateway, mensageria).
- **OK quando:** procedimento e cronograma (ou gatilho) definidos.
- **Referência:** [repositorio-e-ambiente.md#5-no-servidor](repositorio-e-ambiente.md#5-no-servidor) · ASVS V13.3.4.
- **Mapeamento:** nível L3 · Top 10 A02:2025 · ASVS V13.1.4 (L3), V13.3.4 (L3).

### SEC-SEG-10 — Token de bootstrap removido após uso
- **Aplica-se quando:** há token de setup inicial.
- **Risco se faltar:** quem obtiver o token reabre o setup.
- **Como verificar:** `ssh $VPS 'grep -cE "^SETUP_TOKEN=.+" <caminho>/.env'` → 0.
- **OK quando:** vazio/ausente.
- **Referência:** [repositorio-e-ambiente.md#5-no-servidor](repositorio-e-ambiente.md#5-no-servidor).
- **Mapeamento:** nível L1 · Top 10 A07:2025 · ASVS V6.4.1 (L1).

### SEC-SEG-11 — Varredura de segredos no CI
- **Aplica-se quando:** há repositório com CI.
- **Risco se faltar:** o próximo vazamento só é notado tarde demais.
- **Como verificar:** procurar gitleaks/trufflehog/secret scanning em `.github/workflows` ou nas configurações do repositório.
- **OK quando:** roda em todo push/PR e bloqueia.
- **Referência:** [repositorio-e-ambiente.md#1-fora-do-git](repositorio-e-ambiente.md#1-fora-do-git).
- **Mapeamento:** nível L2 · Top 10 A03:2025, A02:2025 · ASVS V13.3.1 (L2).
