# Upload: mídia pública × privada, cache e raspagem

> **Revisado em:** 2026-10-07 · **Origem:** conteúdo compilado de fontes públicas (OWASP, ASVS, NIST, CWE, documentação oficial, avisos de CVE e artigos técnicos) — ver [referências](referencias.md). Se a data estiver antiga (> 6 meses) ou o tema envolver versão/CVE, confirme na fonte oficial antes de aplicar.

## 1. Dois roots

- **Público** (`uploads/`): servido direto pelo Nginx, `autoindex off`, nome UUID de 128 bits (ninguém adivinha), log de acesso **dedicado** (responder "quem baixou qual foto" em auditoria LGPD).
- **Privado** (`private_uploads/`, ex.: termo de consentimento digitalizado): **nunca** montado em `StaticFiles` nem no Nginx; servido só por rota autenticada com permissão dedicada; download **e** exibição auditados; `Cache-Control: no-store`; diretório `750`/`700` com dono da conta de serviço.
- O serviço impede que mídia privada vire conteúdo público (ex.: termo usado como capa de post).

## 2. Arquivo público é público por natureza

- Quem tem a URL abre sem sessão — é o que permite a vitrine funcionar.
- 🔴 `Cache-Control: public, immutable, 30d` torna foto publicada por engano **não recolhível** só apagando o arquivo (CDN e navegadores guardam). Para mídia sensível, cache curto.
- Mídia com acesso restrito exige **rota autenticada** ou **URL assinada de curta duração**.

## 3. Galeria sensível e raspagem

- Gate +18 que vive só no cliente (`useState`; a `<img>` borrada já carrega o `src` real — o blur é CSS) **não é controle de acesso**, é aviso.
- `GET /lista` + `GET /{slug}/media` sem rate limit → acervo baixado com dois `curl` (comprovado: 42 fotos, sem sessão).
- Mitigações reais: UUID; `robots.txt` bloqueando `/uploads/`, `/api/`, `/admin` para `*` **e nominalmente crawlers de IA** (GPTBot, ClaudeBot, CCBot…); sitemap sem slugs sensíveis; capa suprimida e OG neutra em post sensível; metadado separado da mídia.
- Fechar de verdade: **token curto emitido no aceite** exigido em `/{slug}/media` (também gera registro do aceite) + rate limit nos GET públicos + alerta de volume em `uploads.log` (ex.: N imagens por IP por minuto, via jail fail2ban ou cron) + no limite, URL assinada.
- Se for desvio consciente, a decisão precisa estar **assinada por quem responde pelo negócio**, com a consequência explícita: URL vazada entrega a foto para sempre. O consentimento do titular cobre "galeria com aviso", não "acervo raspável".

## 4. Retenção

Revogar o consentimento despublica, mas o arquivo continua no disco **e no backup** — definir prazo
e expurgo (ver [privacidade](../privacidade/README.md)).
