# Vetores de ataque (o golpe que o atacante roda)

> **Revisado em:** 2026-10-07 · **Origem:** conteúdo compilado de fontes públicas (OWASP, ASVS, NIST, CWE, documentação oficial, avisos de CVE e artigos técnicos) — ver [referências](referencias-gerais.md). Se a data estiver antiga (> 6 meses) ou o tema envolver versão/preço/CVE, confirme na fonte oficial antes de aplicar.

> Enquanto [`02-vulnerabilidades.md`](../fundamentos/vulnerabilidades.md) lista **falhas técnicas**, aqui
> ficam **golpes reais**. Vários não exploram bug: exploram regra de negócio ou pessoas.
> Os golpes A01–A11 valem para lojas virtuais e, adaptados, para sites institucionais + CMS.
> Use o 02 no desenvolvimento/code review e este no desenho do produto e na operação.

| | `02-vulnerabilidades` | este documento |
|---|---|---|
| Pergunta | "onde o código pode falhar?" | "qual golpe o atacante roda?" |
| Origem | OWASP / falhas técnicas | fraude e casos reais |

## A01. Card testing (teste de cartões roubados) — *aplica-se se há pagamento com cartão*

- **Como funciona:** bots disparam centenas de compras de baixo valor com cartões roubados para descobrir quais funcionam. Produto digital com entrega imediata (voucher, crédito, assinatura) é o alvo preferido.
- **Prejuízo:** taxa por transação recusada, chargeback, **bloqueio da conta pelo gateway**, reputação.
- **Defesa:** rate limit por IP/conta/pedido no checkout · captcha · *velocity check* · antifraude do gateway ligado · alerta quando a taxa de recusa dispara.
- **Padrão recomendado:** **limite em degraus**, contando só a **recusa confirmada** pela consulta ao gateway (uma vez por pagamento): 1ª e 2ª seguem; da 3ª em diante pede captcha; na 10ª bloqueia com "fale com o SAC" e **código de referência**; janela de 24 h. O **IP tem degraus próprios ~30× maiores** (captcha na 90ª, bloqueio na 300ª) para o CGNAT não bloquear clientes diferentes atrás do mesmo IP. Começa em **modo observar**; números e modo em variável de ambiente. API: 428 pede captcha, 429 traz o código de referência. Visa e Stripe não dão número fixo.
- Relacionado: V13.

## A02. Magecart / web skimming / injeção de script na página

- **Como funciona:** JavaScript malicioso na página (dependência comprometida, script de terceiro — chat, analytics, pixel —, CDN comprometida, painel invadido ou **conteúdo do CMS sem escape**) copia dado digitado ou executa ações. Casos: British Airways, Ticketmaster, Newegg.
- **Decisão de produto:** checkout **hospedado/iframe** tira o campo do cartão da sua página — é o argumento técnico mais forte nessa escolha.
- **Defesa:** CSP rigorosa · **SRI** em scripts externos (quando o fornecedor publica hash estável; senão CSP com allowlist de host) · **zero script de terceiro na página de pagamento** · scripts de analytics só após consentimento · monitorar alteração do front · escapar JSON-LD.
- *Exemplo (site institucional com CMS):* JSON-LD montado com `dangerouslySetInnerHTML={{__html: JSON.stringify(...)}}` com campos do CMS → `</script>` fechava a tag e executava em **todas** as páginas. Corrigido escapando `<`, `>`, `&`.

## A03. Account takeover (ATO) / credential stuffing

- **Como funciona:** listas de e-mail+senha vazadas de outros sites testadas em massa no login.
- **Dano:** rouba valor resgatável (voucher, saldo) e expõe dado sensível → incidente LGPD. Em painel de operador único, a conta é o perímetro inteiro.
- **Defesa:** rate limit + captcha no login · **MFA** (no mínimo em admin e em contas com valor ativo) · detectar login anômalo (aparelho/IP novo) e pedir 2º fator (step-up) · notificar o titular em login novo · bloquear senha sabidamente vazada no cadastro (HIBP k-anonymity) · restringir `/admin` por IP/VPN quando o operador é fixo.

## A04. Fraude de chargeback ("friendly fraud") — *aplica-se se há venda*

- **Como funciona:** o cliente compra, usa o serviço, e contesta alegando não reconhecer.
- **Defesa:** **registro auditável do uso/resgate** (data, hora, unidade, quem validou) como prova · termos de venda claros · e-mail de confirmação de uso · antifraude na compra.

## A05. Abuso de regra de negócio

- **Como funciona:** explora a **regra**, não um bug: várias contas para promoção de primeiro acesso, empilhar descontos, resgatar o mesmo item em dois lugares, inflar contador de métrica.
- **Defesa:** validação sempre no servidor · limite por documento (CPF), não por conta · um item = um resgate atômico · regras de promoção testadas contra abuso antes de publicar · contadores públicos com `verify_public_origin` + rate limit (sabendo que `Origin` é forjável fora do navegador).
- *Exemplo (site institucional):* a única regra com efeito colateral eram contadores de view/clique (UPSERT agregado) — dano máximo: número errado no painel.

## A06. Comprometimento do painel administrativo

- **Como funciona:** phishing no funcionário, senha fraca/reaproveitada, sem MFA, sessão roubada.
- **Por que é grave:** o admin publica conteúdo (inclusive script, ver A02), altera preço e acessa dado sensível. Admin comprometido = incidente de dado.
- **Defesa:** **MFA obrigatório** · menor privilégio (nem todo operador vê dado sensível) · log de auditoria de acesso · sessão curta · restrição por IP/VPN · treinamento antiphishing · `/docs` desligado · CSRF no router inteiro.

## A07. Supply chain (dependência comprometida)

- **Como funciona:** biblioteca npm/pip passa a incluir código malicioso. Casos: `event-stream`, `ua-parser-js`, `xz-utils`.
- **Agravante comum:** build rodando **na VPS de produção** — o pacote hostil executa com as credenciais do servidor.
- **Defesa:** lockfile commitado e `npm ci` · auditoria no CI · revisar o que a atualização traz · Dependabot com major isolado · minimizar dependências no front · SRI · build em runner descartável quando possível.

## A08. Vazamento em massa por API / raspagem de acervo

- **Como funciona:** iterar IDs (`/api/pedidos/1`, `/2`…) ou enumerar uma listagem pública e baixar tudo.
- **Variante "por design" (exemplo: clínica com fotos sensíveis de pacientes):** galeria pública de fotos sensíveis com aviso +18 só no cliente; `GET /api/results` + `GET /api/results/{slug}/media` sem rate limit baixavam o acervo inteiro com dois `curl`. Não é IDOR — é enumeração permitida pelo desenho.
- **Defesa:** autorização por dono em todo endpoint · IDs não sequenciais · rate limit na API **inclusive nos GET públicos** · alerta para volume anômalo de leitura/download · contrapartida de servidor para gate de conteúdo (token curto emitido no aceite) · URL assinada de curta duração para mídia sensível · `robots.txt` bloqueando `/uploads/` e `/api/` (inclusive crawlers de IA) · sitemap sem slugs sensíveis.

## A09. Manipulação de valores no checkout

- Interceptar e alterar preço/quantidade/desconto. **Defesa:** backend recalcula tudo. Relacionado: V03.

## A10. Bots, scraping e DDoS

- **Como funciona:** raspagem de catálogo/preço; sobrecarga proposital, típica em campanha.
- **Defesa:** rate limit · proteção DDoS do provedor (normalmente só **L3/L4**; L7 pede WAF/CDN como Cloudflare) · cache/CDN/ISR para páginas públicas · fail2ban para scanner.
- ⚠️ Pico legítimo de campanha e ataque L7 são difíceis de distinguir — por isso o rate limit precisa ser medido com navegação real ([rate-limit](../rate-limit/README.md)).

## A11. Engenharia social / BEC

- **Como funciona:** e-mail/WhatsApp se passando por fornecedor, executivo ou pela própria empresa (ex.: golpe de "sinal" cobrado de cliente). Ataca a pessoa, não o sistema.
- **Defesa:** dupla verificação fora de banda para pagamento/alteração bancária · treinamento periódico · **MFA nas contas corporativas** (e-mail, domínio, hospedagem, GitHub, redes sociais) · combinado público do que a empresa nunca pede por WhatsApp.
- Boa prática: formulário de contato **sem backend** (monta deep link `wa.me` e instrui a não incluir dado de saúde) elimina spam de formulário e vazamento por caixa de leads.

## Priorização sugerida

1. Para quem vende produto digital: A01, A02, A03, A04, A06.
2. Para site institucional com dado sensível e painel: A08, A06, A02, A07, A10.
