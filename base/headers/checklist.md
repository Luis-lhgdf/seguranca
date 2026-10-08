# Checklist — Cabeçalhos, CSP e XSS (NAV)

> **Revisado em:** 2026-10-07. Variáveis e regras em [`AGENTS.md`](../../AGENTS.md). Gravação de payload XSS **só em ambiente de teste**.

### SEC-NAV-01 — HSTS ativo
- **Aplica-se quando:** site em HTTPS (sempre).
- **Risco se faltar:** primeiro acesso pode ser interceptado em HTTP.
- **Como verificar:** `curl -sI $SITE | grep -i strict-transport-security`.
- **OK quando:** `max-age` ≥ 1 ano (`includeSubDomains`/`preload` se todos os subdomínios tiverem HTTPS).
- **Referência:** [cabecalhos-de-seguranca.md#1-conjunto-mínimo-nas-páginas-html](cabecalhos-de-seguranca.md#1-conjunto-mínimo-nas-páginas-html) · ASVS V3.4.1.
- **Mapeamento:** nível L1 · Top 10 A04:2025, A02:2025 · ASVS V3.4.1 (L1) · WSTG-CONF-07.

### SEC-NAV-02 — CSP nas páginas HTML
- **Aplica-se quando:** serve HTML.
- **Risco se faltar:** qualquer falha de escape vira script executando no navegador do visitante.
- **Como verificar:** `curl -sI $SITE/ | grep -i content-security-policy` e repetir em `/admin/login` e demais locations.
- **OK quando:** CSP enforcing no HTML (Report-Only conta como PARCIAL), com `frame-ancestors`, `object-src 'none'`, `base-uri`.
- **Referência:** [csp.md#2-como-implantar-sem-quebrar](csp.md#2-como-implantar-sem-quebrar).
- **Mapeamento:** nível L2 · Top 10 A02:2025, A05:2025 · ASVS V3.4.3 (L2).

### SEC-NAV-03 — CSP sem `unsafe-inline` em script (meta)
- **Aplica-se quando:** SEC-NAV-02 se aplica.
- **Risco se faltar:** a CSP não impede XSS inline.
- **Como verificar:** ler `script-src` do header.
- **OK quando:** nonce/hash + `strict-dynamic`; `unsafe-inline` = PARCIAL com justificativa (hidratação).
- **Referência:** [csp.md#3-unsafe-inline--nonce](csp.md#3-unsafe-inline--nonce).
- **Mapeamento:** nível L2 · Top 10 A05:2025 · ASVS V3.4.3 (L2).

### SEC-NAV-04 — `nosniff`, proteção contra frame, Referrer-Policy, Permissions-Policy
- **Aplica-se quando:** serve HTML.
- **Risco se faltar:** clickjacking, vazamento de URL sensível, tipo de arquivo adivinhado.
- **Como verificar:** comando da seção 5 de [cabecalhos-de-seguranca.md](cabecalhos-de-seguranca.md#5-como-verificar).
- **OK quando:** os quatro presentes em todas as locations.
- **Referência:** [cabecalhos-de-seguranca.md#1-conjunto-mínimo-nas-páginas-html](cabecalhos-de-seguranca.md#1-conjunto-mínimo-nas-páginas-html) · ASVS V3.4.
- **Mapeamento:** nível L2 · Top 10 A02:2025 · ASVS V3.4.4 (L2), V3.4.5 (L2), V3.4.6 (L2) · WSTG-CLNT-09.

### SEC-NAV-05 — Headers repetidos em todo `location` do Nginx
- **Aplica-se quando:** Nginx com `add_header` dentro de `location`.
- **Risco se faltar:** rotas como `/uploads/` ficam sem nenhum header de segurança.
- **Como verificar:** `ssh $VPS 'sudo nginx -T' | grep -nE "location|add_header"`; `curl -sI` em cada location.
- **OK quando:** todas as locations devolvem o conjunto completo.
- **Referência:** [cabecalhos-de-seguranca.md#3-armadilha-do-nginx-add_header-não-herda](cabecalhos-de-seguranca.md#3-armadilha-do-nginx-add_header-não-herda).
- **Mapeamento:** nível L1 · Top 10 A02:2025 · ASVS V3.4.1 (L1), V3.4.4 (L2).

### SEC-NAV-06 — `Cache-Control: no-store` em resposta autenticada/com PII
- **Aplica-se quando:** há área autenticada ou rota com dado pessoal.
- **Risco se faltar:** dado sensível fica gravado no disco do navegador ou em proxy.
- **Como verificar:** em teste logado, `curl -sI -b <cookie de teste> $API/<rota autenticada> | grep -i cache-control`; `grep -rn "no-store" $REPO`.
- **OK quando:** `no-store` em toda resposta autenticada e em arquivo privado.
- **Referência:** [cabecalhos-de-seguranca.md#2-cache-control-em-resposta-sensível](cabecalhos-de-seguranca.md#2-cache-control-em-resposta-sensível) · ASVS V14.3.2.
- **Mapeamento:** nível L2 · Top 10 A02:2025 · ASVS V14.3.2 (L2) · WSTG-ATHN-06.

### SEC-NAV-07 — Sem versão de servidor/framework nos headers
- **Aplica-se quando:** sempre.
- **Risco se faltar:** facilita mirar CVE da versão exata.
- **Como verificar:** `curl -sI $SITE | grep -iE "^server:|x-powered-by"`.
- **OK quando:** sem número de versão; sem `X-Powered-By`.
- **Referência:** [cabecalhos-de-seguranca.md#1-conjunto-mínimo-nas-páginas-html](cabecalhos-de-seguranca.md#1-conjunto-mínimo-nas-páginas-html).
- **Mapeamento:** nível L3 · Top 10 A02:2025 · ASVS V13.4.6 (L3) · WSTG-INFO-02, WSTG-INFO-08.

### SEC-NAV-08 — Nenhum sink de HTML com conteúdo controlável
- **Aplica-se quando:** front renderiza conteúdo de usuário/CMS.
- **Risco se faltar:** XSS armazenado atingindo todos os visitantes.
- **Como verificar:** greps da seção 3 de [xss-e-escape.md](xss-e-escape.md#3-outros-sinks-a-procurar); analisar cada ocorrência.
- **OK quando:** nenhum sink com dado controlável sem escape.
- **Referência:** [xss-e-escape.md#1-regra](xss-e-escape.md#1-regra) · ASVS V1.2.1, V3.2.
- **Mapeamento:** nível L1 · Top 10 A05:2025 · ASVS V1.2.1 (L1), V1.3.1 (L1), V3.2.2 (L1) · WSTG-INPV-01, WSTG-INPV-02, WSTG-CLNT-01.

### SEC-NAV-09 — JSON em `<script>` escapado
- **Aplica-se quando:** há JSON-LD ou estado serializado em `<script>`.
- **Risco se faltar:** `</script>` num campo do CMS executa código em todas as páginas.
- **Como verificar:** ler o componente; em produção, conferir que o `ld+json` servido não contém `<` cru dentro de valores.
- **OK quando:** `<`, `>`, `&` escapados.
- **Referência:** [xss-e-escape.md#2-caso-típico--xss-armazenado-no-json-ld](xss-e-escape.md#2-caso-típico--xss-armazenado-no-json-ld).
- **Mapeamento:** nível L1 · Top 10 A05:2025 · ASVS V1.2.3 (L1) · WSTG-CLNT-01.

### SEC-NAV-10 — URLs do CMS/usuário com esquema validado
- **Aplica-se quando:** campo de URL vira `href`/`src`.
- **Risco se faltar:** link `javascript:` executa ao clicar.
- **Como verificar:** listar campos de URL nos schemas (tipo `str` cru?); em teste, gravar `javascript:alert(1)` → 422.
- **OK quando:** validação de esquema no backend.
- **Referência:** [xss-e-escape.md#1-regra](xss-e-escape.md#1-regra).
- **Mapeamento:** nível L1 · Top 10 A05:2025 · ASVS V1.2.2 (L1) · WSTG-CLNT-01, WSTG-CLNT-04.

### SEC-NAV-11 — Scripts de terceiros mínimos, após consentimento, com SRI/CSP
- **Aplica-se quando:** há analytics, pixel, chat, CDN.
- **Risco se faltar:** script de terceiro comprometido rouba dados (Magecart).
- **Como verificar:** listar `<script src>` externos nas páginas (`curl -s $SITE | grep -oE '<script[^>]+src="https?://[^"]+'`); conferir carregamento só após consentimento; página de pagamento sem terceiros.
- **OK quando:** inventário mínimo, consentimento respeitado, SRI ou allowlist na CSP.
- **Referência:** [csp.md#5-sri-em-script-externo](csp.md#5-sri-em-script-externo).
- **Mapeamento:** nível L2 · Top 10 A08:2025, A03:2025 · ASVS V3.6.1 (L3), V14.2.3 (L2).

### SEC-NAV-12 — Exportações protegidas contra fórmula (CSV)
- **Aplica-se quando:** o sistema exporta CSV/planilha.
- **Risco se faltar:** fórmula maliciosa executa no Excel de quem abre o relatório.
- **Como verificar:** ler o código de exportação; em teste, gravar `=1+1` e exportar.
- **OK quando:** valores iniciados por `= + - @` neutralizados.
- **Referência:** [xss-e-escape.md#1-regra](xss-e-escape.md#1-regra) · ASVS V1.2.10.
- **Mapeamento:** nível L3 · Top 10 A05:2025 · ASVS V1.2.10 (L3).
