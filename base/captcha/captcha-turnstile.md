# Captcha (Cloudflare Turnstile): quando usar, como configurar, quando NÃO usar

> **Revisado em:** 2026-10-07 · **Origem:** conteúdo compilado de fontes públicas (OWASP, ASVS, NIST, CWE, documentação oficial, avisos de CVE e artigos técnicos) — ver [referências](referencias.md). Se a data estiver antiga (> 6 meses) ou o tema envolver versão/preço/CVE, confirme na fonte oficial antes de aplicar.

> Duas abordagens válidas: **instalar** Turnstile em todas as rotas públicas de escrita (quando
> existe formulário público que poste no backend — ex.: loja virtual com cadastro, login e OTP) ou
> **não instalar** (quando não há formulário público — ex.: site institucional cuja captação sai
> por link externo). A primeira cobra fricção e script de terceiro; a segunda exige registrar os
> gatilhos de reentrada. A regra geral está na §1.

## 1. Precisa de captcha? (decisão)

Captcha é **pedágio cobrado de humano que envia formulário**. Aplica-se quando existe **rota
pública de escrita que um humano envia** e cujo abuso tem custo:

| Rota | Captcha? |
|---|---|
| cadastro, "esqueci a senha", reenvio/envio de OTP, agendamento, cupom, checkout | **sim** |
| login | sim, mas é a camada **menos decisiva** (rate limit + Argon2id seguram tentativa de senha). Painel de operador único: restringir `/admin` por IP é mais barato e eficaz |
| beacons automáticos (contador de view/clique, sem interação humana) | **não** — não há onde encaixar o desafio; custaria script de terceiro em toda página |
| GET público cacheável | **não** — quebraria o cache sem proteger nada |
| bootstrap do 1º admin já fail-closed | não acrescenta |

**N/A legítimo (exemplo: site institucional com painel de operador único):** sem cadastro, login público, OTP, contato com backend,
agendamento ou checkout — a captação sai por link `wa.me`. Os únicos POSTs públicos eram
contadores agregados (UPSERT: abuso não cresce tabela, não gasta dinheiro).

**Gatilhos que reabrem a decisão:** surgir formulário público que poste no backend (principal —
o desafio entra **junto** com o formulário, não depois); endpoint que gasta dinheiro/dispara
mensagem; poluição de métrica **observada**; credential stuffing observado no login; painel com
mais de um operador ou cadastro self-service; abuso volumétrico que o fail2ban não segura (aí a
resposta é WAF/proxy, não captcha).

⚠️ OWASP: captcha **não é o primeiro controle contra cadastro falso** (é *last-resort step-up*);
**não substitui o rate limit — soma**. Bot que resolve captcha existe; o captcha **encarece**
(serviço de resolução cobra por mil e é lento), não impede.

## 2. Por que Turnstile e não reCAPTCHA

- reCAPTCHA clássico **não emite mais chave nova**; virou produto do Google Cloud Fraud Defense, com projeto Cloud e faturamento.
- 🔴 **Motivo real:** sem faturamento, estourada a cota (10 000/mês; teto de 60 000 req/min → **~10 s de tráfego queimam o mês**), o `siteverify` devolve **HTTP 200 com score estático 0,9** e aprova todo mundo — em silêncio. Com faturamento, funciona sem teto de custo (10 001–100 000: US$ 8 fixo; acima: US$ 0,001/avaliação; 1 milhão ≈ US$ 908).
- Turnstile Free: **desafios e verificações ilimitados**, 20 widgets, 10 hostnames por widget, 7 dias de analytics; não usa cookie para coletar dado; Cloudflare se declara operadora. Enterprise: preço sob contrato (não publicado).
- ❌ **Não ter captcha de reserva** (ex.: Google como backup): o widget nem carrega se a Cloudflare cai; máquina de estados no caminho crítico; código que só roda no pior dia; e o reserva sem faturamento aprova todo mundo. O que resolve é **degradação controlada** (§6).

## 3. Fluxo e ordem

1. Navegador resolve o widget → recebe token.
2. Front envia formulário + token.
3. **Backend** chama `siteverify` e só então processa. 🔴 É o único passo que importa.

Ordem no backend: validação de tamanho (`max_length=2048`, campo obrigatório) → `siteverify`
(timeout ~3 s) → trabalho caro (Argon2, banco). Requisição recusada não gasta hash nem rede.

## 4. Achados medidos contra a API real (valem para qualquer projeto)

| Envio | Resultado |
|---|---|
| secret de teste "passa" + token qualquer | `200` · `success: true` · **`metadata.result_with_testing_key: true`** |
| 🔴 **token lixo** com secret de teste | `200` · **`success: true`** |
| secret "falha" | `200` · `success:false` · `invalid-input-response` |
| secret "token já gasto" | `200` · `success:false` · `timeout-or-duplicate` |
| token vazio | `200` · `success:false` · `missing-input-response` |
| 🔴 **sem `secret`** ou **secret inexistente** | **HTTP 400**, não JSON com `error-codes` |

Consequências no código:
- **Guard:** em produção, `result_with_testing_key` presente = subiu com chave de teste → bloqueia e alerta (senão o captcha aprova 100%).
- **Tratar HTTP 400 antes de ler o JSON** (`resposta.json()["success"]` levanta exceção).
- **Conferir `hostname`** da resposta contra a lista do ambiente — a sitekey é pública; sem isso, quem copiar a sitekey gera token válido.
- **Conferir `action`** da resposta = rota chamada.
- **Token de uso único:** renovar o token (`turnstile.reset()`) **depois de toda tentativa**, deu certo ou não. *Bug comum:* errar a senha uma vez travava o login — o widget mostrava "Sucesso!" e o backend respondia `timeout-or-duplicate`.
- Settings **recusa subir em produção** sem chave, com chave de teste ou com `localhost` nos hostnames.

| Código | Resposta |
|---|---|
| `missing-input-response` | 422 |
| `invalid-input-response` (inválido/expirado) | 422 "tente de novo" |
| `timeout-or-duplicate` | 422 (replay; widget gera outro) |
| `bad-request` | 500 nosso (bug) |
| `missing/invalid-input-secret` (chega como HTTP 400) | 500 + **alerta** |
| `internal-error` | ver §6 |

## 5. Configuração

**Front:** script **só** de `https://challenges.cloudflare.com/turnstile/v0/api.js` (não proxiar,
não pôr no bundle); modo **Managed** (o `invisible` obriga citar o *Turnstile Privacy Addendum* na
política de privacidade); **renderização explícita** (`turnstile.render()`) em SPA/React — a
implícita não sobrevive a re-render; isolar em ilha client para manter a página cacheável;
`action` por rota; `theme: auto`; `size: flexible`; `error-callback` e `expired-callback`
obrigatórios (token expira em 5 min); botão **"Tentar de novo"** chamando `reset()`.

**Back:** `secret` só no servidor; `response`; `remoteip` = **IP real do cliente** — atrás do
proxy da Cloudflare é `CF-Connecting-IP`; **sem** proxy Cloudflare (TLS terminando no próprio
Nginx) é o `X-Real-IP`/`X-Forwarded-For` carimbado pelo **seu** proxy; `idempotency_key` (UUID)
para repetir com segurança.

**CSP:** `script-src https://challenges.cloudflare.com` e `frame-src https://challenges.cloudflare.com`;
preferir **nonce** + `strict-dynamic` a `unsafe-inline`.

**Painel:** **um widget por ambiente** (dev com `localhost`; produção só com o domínio real). Com
um só, o hostname de produção aceitaria `localhost` e qualquer pessoa validaria token da sua chave
a partir da própria máquina.

**Chaves de teste** (públicas, documentadas pela Cloudflare; funcionam em qualquer domínio):

| Sitekey | | Secret | |
|---|---|---|---|
| `1x00000000000000000000AA` | passa | `1x0000000000000000000000000000000AA` | valida |
| `2x00000000000000000000AB` | falha | `2x0000000000000000000000000000000AA` | reprova |
| `3x00000000000000000000FF` | força desafio | `3x0000000000000000000000000000000AA` | `timeout-or-duplicate` |

## 6. Quando o `siteverify` falhar (fail-open × fail-closed)

A pessoa não reprovou — **nós não conseguimos perguntar**. Critério: **o que dá para desfazer**.

| Rota | Na dúvida | Por quê |
|---|---|---|
| Cadastro | 🔒 recusa (503 "tente em minutos") | trancar atrasa (reversível); destrancar = milhares de contas falsas |
| OTP / e-mail / SMS | 🔒 recusa | **mensagem enviada é dinheiro gasto — irreversível**; e com cadastro fechado ninguém legítimo pede OTP |
| Login | 🔓 passa, com **rate limit apertado** (ex.: 5 → 2) | trancar deixa todo cliente fora; rate limit + Argon2id seguram |

- Timeout curto (~3 s); **nunca em silêncio**: contador próprio + alerta em toda falha.
- Teste que prova: mock da Cloudflare estourando timeout → cadastro recusa, login passa com limite menor, contador sobe.
- Por que não "deixar passar e confiar no rate limit": rate limit por IP é **divisão, não teto** — 10 000 IPs residenciais × 10 req = 100 000 chamadas sem violar o limite uma vez; no OTP de pré-cadastro a identidade é o telefone que o atacante escolhe.

## 7. Ao testar

- **DevTools aberto reprova o desafio** (erro `600010`, família "bot behavior detected": Puppeteer/Playwright usam o mesmo protocolo CDP). Fechar o DevTools depois de ajustar a largura.
- Celular de verdade: `127.0.0.1` não serve; adicionar o IP da máquina na rede aos hostnames do widget de dev.
- Falha por rede/IP específico (VPN, rede corporativa) acontece com cliente real — por isso o botão "Tentar de novo".

## 8. Privacidade

A escolha entra na **Política de Privacidade** e no banner de cookies. Ephemeral ID (Enterprise)
é fingerprint → reabre pauta LGPD.
