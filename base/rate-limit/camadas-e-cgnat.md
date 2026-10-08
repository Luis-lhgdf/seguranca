# Rate limit: camadas, CGNAT e o erro de configurar sem testar

> **Revisado em:** 2026-10-07 · **Origem:** conteúdo compilado de fontes públicas (OWASP, ASVS, NIST, CWE, documentação oficial, avisos de CVE e artigos técnicos) — ver [referências](referencias.md). Inclui lição de incidente real relatado publicamente. Se a data estiver antiga (> 6 meses), confirme na fonte oficial antes de aplicar.

> *"Segurança não é o que você configura, é o que você testa com gente de verdade acessando."*
> *"Overcorrection é o novo downtime."*

## 1. O incidente

Um SaaS sobreviveu a um DDoS real (260 milhões de requests num dia) e depois foi **derrubado pelo
próprio rate limit** configurado no pânico: 60 req/min por IP. A navegação normal batia no teto.

## 2. Por que limite por IP derruba usuário legítimo

| Causa | O que acontece |
|---|---|
| Uma página = dezenas de requests | listagem com 50 produtos ≈ 50 imagens; uma home deu ~53 requests contra teto de 60 |
| Prefetch | Next.js/Turbo pré-carregam links no hover/viewport — cada um conta |
| **CGNAT** | operadoras brasileiras põem centenas de usuários atrás de um IP; dois clientes na mesma rede somam no mesmo balde |
| SSR | o servidor do Next chama a API a partir de **um só IP** — limite por IP na API pública estrangula o SSR |

## 3. Regras

- **Isentar assets** do limite de ações: `/_next/static/`, `/midia/`, `/uploads/`, `favicon`, `robots.txt` — servidos como estático pelo Nginx, fora do app.
- **Medir o custo real de uma página** (home, listagem, detalhe) antes de escolher número; teto com folga.
- IP **generoso** em rotas de navegação; ações caras (login, OTP, cupom, checkout) combinam IP **e** identidade/sessão. Padrão recomendado: por conta = teto apertado; **por IP = 30×** (≈ 30 usuários atrás de um IP).
- Baldes independentes: a conta que estourou o **seu** teto não leva junto quem divide o IP.
- **Modo observar** antes de bloquear: só registra (`acao=observado`); números saem da observação e do teste de carga.
- Resposta 429 amigável (HTML ou JSON com `Retry-After`), sem revelar o limite exato, com **código de referência** para o suporte.
- Rotas máquina a máquina (ERP/integração) fora do limite de usuário, com teste que prove.

## 4. Camadas

| Camada | Papel |
|---|---|
| CDN/WAF (Cloudflare) | 1ª contra volume: rate limiting rules, *under attack mode*, Bot Fight Mode (começar em *Log*). "IP with NAT support" só em planos acima do básico |
| Provedor da VPS | normalmente só **L3/L4** — 100 000 requests HTTP espalhados em 10 000 IPs não são DDoS volumétrico |
| Nginx `limit_req` | freio fino e **teto real** (único para todos os workers) |
| Aplicação | por identidade/rota; em memória = **por processo** (2 workers = o dobro) → storage compartilhado (Redis) para precisão |
| fail2ban `nginx-limit-req` | bane quem estoura repetidamente |

Atrás de proxy/CDN, o IP real vem do header do proxy **confiável** (`CF-Connecting-IP` com
`set_real_ip_from` restrito às faixas da Cloudflare; ou `X-Forwarded-For` só de `127.0.0.1`).
Sem isso, todo mundo vira o IP do proxy — ou o atacante forja o header.

## 5. Teste

- 🔴 **Regressão:** um teste que simula navegação normal (com prefetch e assets) e prova **zero 429**.
- Rota protegida: N+1 requisições → 429.
- Teste de carga (k6) em pico realista (ex.: Black Friday acima do dimensionado): p95/p99 e erros dentro do limite; 429 = 0 no fluxo legítimo; ISR/cache aliviando o backend.
- Carga **nunca em produção sem autorização explícita**.
