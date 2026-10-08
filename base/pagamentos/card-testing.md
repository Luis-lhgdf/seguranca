# Pagamentos: card testing e limite de recusas

> **Revisado em:** 2026-10-07 · **Origem:** conteúdo compilado de fontes públicas (OWASP, ASVS, NIST, CWE, documentação oficial, avisos de CVE e artigos técnicos) — ver [referências](referencias.md). Se a data estiver antiga (> 6 meses) ou o tema envolver versão/CVE, confirme na fonte oficial antes de aplicar.

## 1. O ataque

Bots testam cartões roubados com compras de baixo valor. Produto digital com entrega imediata é o
alvo preferido. Prejuízo: taxa por transação, chargeback, **bloqueio da conta no gateway**,
reputação. Fontes: Stripe (card testing) e Visa (anti-enumeration, jun/2026) — **nenhuma dá número
fixo**.

## 2. Defesas

- Rate limit por **pedido, conta e IP** no checkout (o cartão em si não é visível se o gateway hospeda o formulário).
- Captcha como degrau, não como primeira barreira.
- *Velocity check* (X tentativas em Y minutos); exigir login antes de pagar.
- Antifraude do gateway **ligado**.
- **Alerta** quando a taxa de recusa dispara.

## 3. Limite em degraus (padrão recomendado)

| Dimensão | Captcha a partir de | Bloqueio em | Janela |
|---|---|---|---|
| Pedido / conta | 3ª recusa | 10ª recusa | 24 h (vida do pedido aberto) |
| IP | 90ª recusa | 300ª recusa | 24 h |

- Conta só a **recusa confirmada** pela consulta ao gateway, **uma vez por pagamento** (`SET NX`), mesmo que conferida pelo aviso, pela varredura e pela tela.
- IP com degraus **30× maiores** que a conta: com CGNAT, 10 clientes recusados atrás do mesmo IP bloqueariam o pagamento de todos ali por 24 h (teste: recusas de contas diferentes no mesmo IP não barram ninguém).
- API: **428** pede o captcha; **429** traz **código de referência** para o SAC; mensagem "fale com o SAC".
- Começa em **modo observar** (só registra o evento); números e modo em variável de ambiente; os números finais saem da observação e do teste de carga, não de estimativa.
- ⚠️ Se a tela do gateway deixa tentar vários cartões no mesmo pagamento, só o desfecho final chega ao seu sistema — confirmar na certificação.

## 4. Relacionados

[rate-limit](../rate-limit/README.md) (CGNAT, modo observar) · [captcha](../captcha/README.md).
