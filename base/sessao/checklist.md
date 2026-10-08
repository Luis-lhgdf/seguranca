# Checklist — Sessão e tokens (SESS)

> **Revisado em:** 2026-10-07. Variáveis e regras em [`AGENTS.md`](../../AGENTS.md).

### SEC-SESS-01 — Cookies de sessão com HttpOnly, Secure e SameSite
- **Aplica-se quando:** a sessão usa cookie.
- **Risco se faltar:** um script injetado rouba a sessão; o cookie viaja sem HTTPS.
- **Como verificar:** em ambiente de teste, `curl -si -X POST $API/<login> -d '<credencial de teste>' | grep -i set-cookie`; ou ler o código que seta o cookie.
- **OK quando:** `HttpOnly; Secure; SameSite=Lax|Strict` em sessão/refresh; path do refresh estreito.
- **Referência:** [tokens-e-cookies.md#2-regras-gerais](tokens-e-cookies.md#2-regras-gerais) · ASVS V3.3.1–V3.3.4.

### SEC-SESS-02 — Nenhum token em localStorage/sessionStorage
- **Aplica-se quando:** há front com sessão.
- **Risco se faltar:** qualquer XSS leva o token.
- **Como verificar:** `grep -rnE "localStorage|sessionStorage" $REPO/<front>` e ler cada uso.
- **OK quando:** nenhum token nem PII em storage do navegador.
- **Referência:** [tokens-e-cookies.md#2-regras-gerais](tokens-e-cookies.md#2-regras-gerais) · ASVS V14.3.3.

### SEC-SESS-03 — Token aleatório forte, nunca derivado de credencial
- **Aplica-se quando:** há sessão, código ou identificador secreto.
- **Risco se faltar:** sessão previsível ou eterna.
- **Como verificar:** `grep -rnE "import random|random\.|uuid1|Math\.random|Date\.now\(\)" $REPO` nos pontos que geram token/código; ler a geração.
- **OK quando:** CSPRNG (`secrets`, `crypto.randomBytes`, `uuid4`) com ≥ 128 bits.
- **Referência:** [tokens-e-cookies.md#2-regras-gerais](tokens-e-cookies.md#2-regras-gerais) · ASVS V7.2.3.

### SEC-SESS-04 — Access curto, sem privilégio no token, algoritmo fixo
- **Aplica-se quando:** usa JWT.
- **Risco se faltar:** token roubado vale muito tempo; privilégio obsoleto; *alg confusion*.
- **Como verificar:** ler emissão (TTL, claims) e decodificação (`algorithms=[...]`, `exp`/`type`).
- **OK quando:** TTL ≤ ~15 min, sem role no token, algoritmo fixo.
- **Referência:** [tokens-e-cookies.md#1-padrão-de-referência](tokens-e-cookies.md#1-padrão-de-referência) · ASVS V9.

### SEC-SESS-05 — Refresh rotativo, guardado como hash, com detecção de reuso
- **Aplica-se quando:** há refresh token.
- **Risco se faltar:** refresh roubado vale por dias sem ninguém notar.
- **Como verificar:** ler o serviço; teste local reapresentando refresh antigo → 401 e família revogada.
- **OK quando:** hash no banco + rotação + revogação da família no reuso.
- **Referência:** [tokens-e-cookies.md#1-padrão-de-referência](tokens-e-cookies.md#1-padrão-de-referência).

### SEC-SESS-06 — Logout e troca de senha/privilégio revogam no servidor
- **Aplica-se quando:** há sessão.
- **Risco se faltar:** sessão continua válida depois de sair ou de trocar a senha.
- **Como verificar:** em teste, logout → reusar refresh/sessão → 401; trocar senha → sessões antigas → 401.
- **OK quando:** revogação real; gap do access JWT (até expirar) documentado.
- **Referência:** [tokens-e-cookies.md#2-regras-gerais](tokens-e-cookies.md#2-regras-gerais).

### SEC-SESS-07 — Purga de sessões/tokens agendada
- **Aplica-se quando:** tokens/sessões ficam em banco.
- **Risco se faltar:** tabela cresce com tokens velhos e dado pessoal (IP, user-agent).
- **Como verificar:** `ssh $VPS 'systemctl list-timers --all; sudo crontab -l; ls /etc/cron.d'`.
- **OK quando:** job agendado e rodando.
- **Referência:** [tokens-e-cookies.md#1-padrão-de-referência](tokens-e-cookies.md#1-padrão-de-referência).

### SEC-SESS-08 — CSRF em toda rota que muda estado
- **Aplica-se quando:** sessão por cookie.
- **Risco se faltar:** outro site faz o usuário logado executar ações.
- **Como verificar:** listar routers mutáveis e conferir a dependência CSRF no router; em teste, POST autenticado sem o header → 403.
- **OK quando:** todo router mutável protegido; exceções escritas no código.
- **Referência:** [tokens-e-cookies.md#3-csrf](tokens-e-cookies.md#3-csrf) · ASVS V3.5.1–V3.5.3.

### SEC-SESS-09 — Ações públicas com efeito colateral conferem a origem
- **Aplica-se quando:** há POST público (contador, beacon, formulário).
- **Risco se faltar:** página hostil dispara a ação no navegador dos visitantes.
- **Como verificar:** `curl -s -o /dev/null -w '%{http_code}' -X POST -H 'Origin: https://evil.example' $API/<rota>` → 403 (rota idempotente/inofensiva; senão, só em teste).
- **OK quando:** origem estranha recusada + rate limit.
- **Referência:** [tokens-e-cookies.md#3-csrf](tokens-e-cookies.md#3-csrf).

### SEC-SESS-10 — Segredo de assinatura forte e distinto por ambiente
- **Aplica-se quando:** há JWT/cookie assinado.
- **Risco se faltar:** quem tem o segredo de dev forja sessão de produção.
- **Como verificar:** ler o validador de config (placeholder/tamanho); perguntar ao responsável como o segredo de produção foi gerado (não ler o valor).
- **OK quando:** ≥ 32 chars, gerado no servidor, diferente de dev e do pepper.
- **Referência:** [tokens-e-cookies.md#2-regras-gerais](tokens-e-cookies.md#2-regras-gerais).
