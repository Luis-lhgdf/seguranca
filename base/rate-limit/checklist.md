# Checklist — Rate limit, carga e abuso (RL)

> **Revisado em:** 2026-10-07. Variáveis e regras em [`AGENTS.md`](../../AGENTS.md). **Teste de carga e rajadas só com autorização explícita e fora de produção** (ou em janela combinada).

### SEC-RL-01 — Limite na borda (Nginx/CDN) e na aplicação
- **Aplica-se quando:** há API pública ou login.
- **Risco se faltar:** abuso ilimitado; ou o limite do app vale em dobro por worker.
- **Como verificar:** `ssh $VPS 'sudo nginx -T | grep -nE "limit_req"'`; ler o limiter do app e o storage (memória × Redis).
- **OK quando:** borda com zonas dedicadas + app nas rotas sensíveis; limite em memória documentado.
- **Referência:** [camadas-e-cgnat.md#4-camadas](camadas-e-cgnat.md#4-camadas).
- **Mapeamento:** nível L1 · Top 10 A06:2025 · ASVS V2.4.1 (L2), V6.3.1 (L1) · WSTG-BUSL-07 · API4:2023.

### SEC-RL-02 — Assets fora do limite de ações
- **Aplica-se quando:** há `limit_req` em locations que servem páginas.
- **Risco se faltar:** navegação normal recebe 429.
- **Como verificar:** no `nginx -T`, conferir que `/_next/static/`, `/uploads/`, imagens e `robots.txt` não estão sob a zona de ações.
- **OK quando:** estáticos isentos ou em zona própria folgada.
- **Referência:** [camadas-e-cgnat.md#3-regras](camadas-e-cgnat.md#3-regras).
- **Mapeamento:** nível L2 · Top 10 A06:2025 · ASVS V2.4.1 (L2).

### SEC-RL-03 — Limite por IP compatível com CGNAT
- **Aplica-se quando:** limite por IP em rota usada por clientes.
- **Risco se faltar:** clientes atrás da mesma operadora se bloqueiam entre si.
- **Como verificar:** comparar teto por IP × teto por conta; existe identidade/sessão nas ações caras?
- **OK quando:** IP generoso (≈ 30× a conta) + identidade nas ações caras.
- **Referência:** [camadas-e-cgnat.md#3-regras](camadas-e-cgnat.md#3-regras).
- **Mapeamento:** nível L2 · Top 10 A06:2025 · ASVS V2.4.1 (L2).

### SEC-RL-04 — IP real vindo só do proxy confiável
- **Aplica-se quando:** há Nginx/CDN na frente do app.
- **Risco se faltar:** todos viram o mesmo IP, ou o atacante forja `X-Forwarded-For`.
- **Como verificar:** ler `set_real_ip_from`/`real_ip_header` no Nginx e o `forwarded_allow_ips`/`trust proxy` do app.
- **OK quando:** confia só em `127.0.0.1` ou nas faixas oficiais da CDN.
- **Referência:** [camadas-e-cgnat.md#4-camadas](camadas-e-cgnat.md#4-camadas).
- **Mapeamento:** nível L2 · Top 10 A02:2025 · ASVS V4.1.3 (L2), V15.3.4 (L2).

### SEC-RL-05 — GET públicos que servem acervo têm limite
- **Aplica-se quando:** listagens/mídias públicas de conteúdo sensível ou valioso.
- **Risco se faltar:** raspagem completa em minutos.
- **Como verificar:** listar GET públicos e seus limites; checar se o limite não estrangula o SSR (chave por IP do SSR?).
- **OK quando:** limite adequado ou risco aceito por escrito.
- **Referência:** [camadas-e-cgnat.md#2-por-que-limite-por-ip-derruba-usuário-legítimo](camadas-e-cgnat.md#2-por-que-limite-por-ip-derruba-usuário-legítimo).
- **Mapeamento:** nível L2 · Top 10 A06:2025 · ASVS V2.4.1 (L2) · WSTG-BUSL-07 · API6:2023.

### SEC-RL-06 — Resposta 429 amigável e rastreável
- **Aplica-se quando:** há rate limit.
- **Risco se faltar:** cliente não entende; suporte não acha o caso.
- **Como verificar:** provocar 429 em teste e ler a resposta.
- **OK quando:** `Retry-After`, mensagem clara, código de referência, sem revelar o número exato.
- **Referência:** [camadas-e-cgnat.md#3-regras](camadas-e-cgnat.md#3-regras).
- **Mapeamento:** nível L2 · Top 10 A10:2025 · ASVS V16.5.1 (L2).

### SEC-RL-07 — Teste de regressão: navegação normal sem 429
- **Aplica-se quando:** há rate limit em rotas de navegação.
- **Risco se faltar:** um deploy futuro reintroduz o overcorrection.
- **Como verificar:** procurar teste automatizado que simula navegação (com prefetch/assets) e espera zero 429.
- **OK quando:** existe e roda no CI.
- **Referência:** [camadas-e-cgnat.md#5-teste](camadas-e-cgnat.md#5-teste).
- **Mapeamento:** nível L2 · Top 10 A06:2025 · ASVS V2.4.1 (L2).

### SEC-RL-08 — Teste de carga com pico realista
- **Aplica-se quando:** há campanha/pico previsto ou SLA.
- **Risco se faltar:** o sistema (ou o próprio freio) cai no dia do pico.
- **Como verificar:** procurar scripts k6/relatório recente; se ausente, propor (não executar em produção sem autorização).
- **OK quando:** relatório recente com p95/p99, taxa de erro e 429 = 0 no fluxo legítimo.
- **Referência:** [camadas-e-cgnat.md#5-teste](camadas-e-cgnat.md#5-teste).
- **Mapeamento:** nível L2 · Top 10 A06:2025 · ASVS V15.1.3 (L2), V15.2.2 (L2) · API4:2023.

### SEC-RL-09 — Proteção L7 / WAF avaliada
- **Aplica-se quando:** site público com risco de pico hostil ou scraping.
- **Risco se faltar:** só L3/L4 do provedor; L7 descoberto.
- **Como verificar:** `dig +short <dominio>` / headers `cf-ray`, `server: cloudflare`; perguntar sobre WAF.
- **OK quando:** CDN/WAF na frente ou decisão escrita de não usar.
- **Referência:** [camadas-e-cgnat.md#4-camadas](camadas-e-cgnat.md#4-camadas).
- **Mapeamento:** nível L2 · Top 10 A02:2025 · ASVS V2.4.1 (L2).

### SEC-RL-10 — Modo observar antes de bloquear limites novos
- **Aplica-se quando:** limite novo ou alterado em rota de cliente.
- **Risco se faltar:** bloquear clientes reais com número chutado.
- **Como verificar:** procurar flag `observar/aplicar` e o evento registrado.
- **OK quando:** limites novos nascem observando, com número final vindo de dado.
- **Referência:** [camadas-e-cgnat.md#3-regras](camadas-e-cgnat.md#3-regras).
- **Mapeamento:** Top 10 A06:2025 · sem requisito ASVS direto.
