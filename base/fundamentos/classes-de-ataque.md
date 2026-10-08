# Classes de ataque vistas em casos reais

> **Revisado em:** 2026-10-07 · **Origem:** conteúdo compilado de fontes públicas (OWASP, ASVS, NIST, CWE, documentação oficial, avisos de CVE e artigos técnicos) — ver [referências](referencias-gerais.md). Se a data estiver antiga (> 6 meses) ou o tema envolver versão/preço/CVE, confirme na fonte oficial antes de aplicar.

> Destilado de material público (síntese de ~27 vídeos de exploração real de apps — canais de
> hacking ético brasileiros). Aqui fica a **mecânica** de cada classe e a defesa, para o agente
> reconhecer o padrão em qualquer stack, incluindo classes menos lembradas (SVG, tipo trocado,
> segredo entre ambientes, semente previsível, tracker de IP, honeypot).

## 1. Autorização e controle de acesso

| Classe | Mecânica | Defesa |
|---|---|---|
| IDOR sequencial / API sem autenticação | trocar ID numérico em API exposta | autenticação + dono do recurso; UUID |
| `user_id` lido do **corpo** em vez da sessão | atualizar perfil de outro mandando o id dele | identidade sempre da sessão/token |
| "Autenticação" por `user_id` no body | criar sessão só com o id | sessão emitida após prova de credencial |
| BFLA / role no cliente | trocar `student` → `admin` em JSON/LocalStorage/Burp Match&Replace | papel relido do banco no servidor a cada request; JWT sem claim de privilégio |
| Painel escondido só no roteamento do front, credencial no bundle | `admin_logado: true` no LocalStorage | autorização na API; nada de segredo no bundle |
| Bypass de redirecionamento client-side | validação de acesso só no front após carregar | servidor nega |
| Banco exposto ao cliente sem RLS (ex.: Supabase/PostgREST, RPC exposta) | query arbitrária em tabela de terceiros | RLS obrigatório **ou** banco só atrás da API |
| Bypass de middleware (Next.js CVE-2025-29927, header `X-Middleware-Subrequest`) | forjar header para pular o middleware de auth | atualizar o framework; **middleware não é a autenticação** — a API autoriza em toda requisição |
| Bypass de 2FA manipulando a resposta (401 → 200) / `TFA_enabled:false` no payload | o cliente decide | o servidor decide; estado do 2FA não vem do cliente |
| Rota admin sem auth (`/admin/config/bd.php`) | POST direto | autenticação em toda rota administrativa |

## 2. Lógica de negócio e concorrência

| Classe | Mecânica | Defesa |
|---|---|---|
| Race condition (TOCTOU) em reembolso/saldo/compra | requisições paralelas multiplicam saldo | transação atômica, row lock, incremento atômico |
| Mass assignment de preço | campo extra (preço) num formulário de avaliação | whitelist de campos |
| Preço/valor do Pix definido pelo front (`amount`) | gerar cobrança com valor do cliente | recalcular no servidor |
| "Released" no cliente | `released:false → true` libera conteúdo | regra de tempo/liberação no servidor; conteúdo bloqueado não é enviado |
| Regra de jogo no cliente (moedas em hex, `game_over`, velocidade) / WebSocket sem validação | o cliente reporta o resultado | servidor valida limites e estado |

## 3. Entrada e tipo

| Classe | Mecânica | Defesa |
|---|---|---|
| **DoS por ponto flutuante / `NaN`** | `1.5` em campo de estrelas cria array de tamanho fracionado e derruba o runtime; coordenada `7.5` fura checagem | schema com tipagem estrita (Zod/Joi/Pydantic): inteiro é inteiro |
| Payload gigante | encher/poluir o banco | `max_length` em tudo + limite de corpo |
| Filtro de XSS por palavra | banir `<script>` minúsculo | escape no destino; nunca blocklist |

## 4. Frontend e XSS

| Classe | Mecânica | Defesa |
|---|---|---|
| **XSS via upload de SVG** | `<script>` dentro de SVG de foto de perfil, servido no mesmo domínio | SVG fora da allowlist; magic bytes; `nosniff`; CSP |
| XSS por interpolação/template string | `${expression}` em string com crases renderizada | não avaliar conteúdo de usuário; CSP |
| **XSS por quebra de contexto `<script>` (JSON-LD)** | `JSON.stringify` não escapa `<`, `>`, `/` → `</script>` fecha a tag | escapar `<` `>` `&` como `<` `>` `&` |
| HTML personalizado em banner | campo admin aceita tags | escape; allowlist |
| **Tracker de IP por imagem externa** | URL de imagem externa em perfil revela o IP de quem vê | allowlist de host de imagem; `remotePatterns: []` |
| Chave AES hardcoded no bundle | descriptografar resposta da API no cliente | nunca segredo no front |

## 5. Segredos, criptografia e infraestrutura

| Classe | Mecânica | Defesa |
|---|---|---|
| `.env`/chave no git (inclusive commit de IA/"teste") | histórico recuperável | `.gitignore` + gitleaks/trufflehog no CI |
| `.env` exposto na web | GET `/.env` | não servir dotfiles (`location ~ /\.` → deny) |
| Chave privada de gateway no código público | interceptar saques/split | segredo só no backend; rotação |
| **Mesmo segredo entre ambientes** (JWT/pepper) | forjar token de produção a partir de homologação | segredos gerados por ambiente, no servidor |
| **Semente previsível** (timestamp, `random`/Mersenne Twister, `uuid1`) | prever token/código/resultado | CSPRNG (`secrets`, `crypto.randomUUID`, `uuid4`) |
| Hash rápido sem salt / senha em texto puro / cifra fraca | rainbow table, brute force | Argon2id + salt + pepper ([autenticacao/senhas-hash-e-pepper](../autenticacao/senhas-hash-e-pepper.md)) |
| Senha como token | SHA-256 da senha como sessão | token opaco aleatório ou JWT curto |
| JWT sem revogação | não dá para invalidar | TTL curto + refresh rotativo com detecção de reuso |
| Porta de serviço exposta (port scanning) | serviço achado na internet | firewall default deny; só 22/80/443 |
| Backdoor em template comprado | código malicioso do fornecedor | revisar código de terceiro; não usar template de origem duvidosa |
| File carving / formatação rápida | blocos continuam no disco após "formatar" | overwrite/zero-fill antes de descartar mídia (procedimento de infra) |

## 6. Abuso e automação

| Classe | Defesa |
|---|---|
| Sem rate limit/captcha em cadastro, login, **OTP admin de 4 dígitos** | rate limit por IP e identidade; captcha; OTP ≥ 6 dígitos com teto de palpites |
| Bypass de rate limit por rede distribuída (rotação de IP/tokens) | limite por identidade + captcha + alarme de conversão; IP é só uma dimensão |
| Self-bot/scraping com token de usuário | rate limit por conta; detecção de padrão |
| Data poisoning (modelo que aprende com input sem moderação) | moderar/validar o que alimenta o modelo — **só se houver IA treinando com input** |

## 7. Defesa ativa — honeypot

Rotas falsas (`/admin.php`, `/wp-login.php`, `/config.php`, `/.env`) e campos invisíveis que
nenhum humano toca: quem bate ali é scanner. Implementação barata: `location` de isca no Nginx
retornando 403/404 com `access_log` próprio + jail do fail2ban sobre esse log → ban preventivo.
Observação: anunciar `/admin` como `disallow` no `robots.txt` informa ao scanner onde fica
o painel — a isca compensa. Pode-se desautorizar a rota-isca no `robots.txt` (humano legítimo não
acessa; scanner que ignora o robots é identificado).

## 8. Descartes típicos (registrar como N/A com motivo)

Supabase/RLS sem Supabase; WebSocket sem WebSocket; regra de jogo sem jogo; data poisoning sem IA;
Minecraft/SLP sem servidor de jogo; file carving em app web (é procedimento de descarte de disco).
