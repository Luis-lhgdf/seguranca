# Pagamentos: checkout, webhook e idempotência

> **Revisado em:** 2026-10-07 · **Origem:** conteúdo compilado de fontes públicas (OWASP, ASVS, NIST, CWE, documentação oficial, avisos de CVE e artigos técnicos) — ver [referências](referencias.md). Se a data estiver antiga (> 6 meses) ou o tema envolver versão/CVE, confirme na fonte oficial antes de aplicar.

## 1. Escopo PCI

- Deixar o **gateway processar o cartão** (checkout hospedado, iframe ou tokenização): o campo do cartão não fica na sua página → escopo **SAQ A/A-EP** e Magecart perde o alvo. É o argumento técnico mais forte na escolha hospedado × transparente.
- **Nunca** armazenar PAN, CVV ou trilha. Guardar só token/ID do gateway.
- Página de pagamento: **zero script de terceiro**; CSP com os domínios do gateway e do captcha, sem `unsafe-inline`.
- Chave do lojista (`merchant_key`, secret) **só no backend**.

## 2. Valor sempre do servidor

- O backend recalcula preço, desconto e total a partir do banco; ignora valor vindo do cliente (inclusive `amount` ao gerar Pix).
- Teste: interceptar o checkout e trocar preço → pedido com preço correto ou recusado.

## 3. Webhook / notificação do gateway

Três camadas — a **2ª é obrigatória**:
1. **Assinatura** (HMAC) por mensagem quando o gateway documenta (ASVS V4.1.5, L3). Se não documenta, registrar "a confirmar com o gateway".
2. **Nunca confiar no payload:** consultar o status na API do gateway pelo ID antes de emitir qualquer coisa. Funciona mesmo sem assinatura.
3. **Idempotência:** guardar `event_id`/ID do pagamento processado; repetição é ignorada (ASVS V2.3.4).

Também: rota de webhook com teto de corpo e rate limit; varredura periódica dos pendentes (o
aviso pode não chegar) usando a **mesma** função idempotente.

Teste: POST forjado "pago" → nada emitido; mesmo evento 3× → 1 efeito.

## 4. Estados e atomicidade

- Estados do pedido/voucher definidos e auditáveis; transições só pelo servidor.
- Emissão e uso de voucher/crédito em transação atômica (ver [banco](../banco/consultas-e-transacoes.md#2-concorrência-toctou-e-idempotência)).
- Estorno ≤ valor pago; voucher usado não reativa; registro de **quem/quando/onde** do resgate (prova contra chargeback "friendly fraud").
- Aprovação dupla (four-eyes) para reembolso manual acima de um valor (ASVS V2.3.5) — pode morar no sistema de SAC/financeiro que consome a API; emissão manual de crédito idealmente **não existe**.
- Conciliação diária: valor liquidado × vendido.

## 5. Comunicação com o gateway

- Limite de conexões concorrentes documentado (ASVS V13.1.2) para não esgotar a integração.
- Timeouts e retentativas idempotentes.
- Credencial de produção distinta da de homologação.
