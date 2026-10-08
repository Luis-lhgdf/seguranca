# Checklist — Pagamentos (PAG)

> **Revisado em:** 2026-10-07. Variáveis e regras em [`AGENTS.md`](../../AGENTS.md). **Nunca** disparar pagamento real nem webhook forjado em produção: só em homologação/sandbox.

### SEC-PAG-01 — Cartão processado pelo gateway, nunca armazenado
- **Aplica-se quando:** aceita cartão.
- **Risco se faltar:** escopo PCI completo e roubo de cartões na própria página.
- **Como verificar:** ver se o checkout é hospedado/iframe/tokenizado; `grep -rniE "card_number|pan|cvv|cvc" $REPO/<backend>` e no schema do banco.
- **OK quando:** dado de cartão nunca passa pelo seu backend nem banco.
- **Referência:** [checkout-e-webhook.md#1-escopo-pci](checkout-e-webhook.md#1-escopo-pci).

### SEC-PAG-02 — Valor recalculado no servidor
- **Aplica-se quando:** há cobrança.
- **Risco se faltar:** comprar algo de R$ 800 por R$ 0,50.
- **Como verificar:** ler a criação do pedido/cobrança (preço vem do banco?); em sandbox, alterar o preço na requisição.
- **OK quando:** valor do cliente ignorado.
- **Referência:** [checkout-e-webhook.md#2-valor-sempre-do-servidor](checkout-e-webhook.md#2-valor-sempre-do-servidor) · ASVS V2.2.2.

### SEC-PAG-03 — Webhook revalida o status na API do gateway
- **Aplica-se quando:** recebe notificação de pagamento.
- **Risco se faltar:** um POST falso "confirma" pagamento inexistente.
- **Como verificar:** ler o handler: consulta o gateway pelo ID antes de agir? valida assinatura quando existe?
- **OK quando:** revalidação obrigatória (+ assinatura se disponível).
- **Referência:** [checkout-e-webhook.md#3-webhook--notificação-do-gateway](checkout-e-webhook.md#3-webhook--notificação-do-gateway) · ASVS V4.1.5.

### SEC-PAG-04 — Idempotência no processamento de pagamento
- **Aplica-se quando:** há webhook, varredura ou retentativa.
- **Risco se faltar:** o mesmo evento gera dois vouchers/créditos.
- **Como verificar:** procurar chave única de evento/pagamento; teste em sandbox: mesmo evento 3× → 1 efeito.
- **OK quando:** efeito único garantido no banco.
- **Referência:** [checkout-e-webhook.md#3-webhook--notificação-do-gateway](checkout-e-webhook.md#3-webhook--notificação-do-gateway) · ASVS V2.3.4.

### SEC-PAG-05 — Emissão/uso de crédito atômicos e auditados
- **Aplica-se quando:** há voucher, crédito, saldo.
- **Risco se faltar:** uso em dobro; sem prova contra chargeback.
- **Como verificar:** ver SEC-BD-03; conferir registro de quem/quando/onde no resgate.
- **OK quando:** atômico + registro completo do uso.
- **Referência:** [checkout-e-webhook.md#4-estados-e-atomicidade](checkout-e-webhook.md#4-estados-e-atomicidade).

### SEC-PAG-06 — Limite de recusas contra card testing
- **Aplica-se quando:** aceita cartão.
- **Risco se faltar:** o checkout vira ferramenta de teste de cartão roubado; gateway bloqueia a conta.
- **Como verificar:** procurar contador de recusas por pedido/conta/IP, degraus de captcha/bloqueio, modo observar.
- **OK quando:** degraus por pedido/conta e IP (IP mais alto por CGNAT) + alerta de taxa de recusa.
- **Referência:** [card-testing.md#3-limite-em-degraus-padrão-recomendado](card-testing.md#3-limite-em-degraus-padrão-recomendado).

### SEC-PAG-07 — Página de pagamento sem scripts de terceiros
- **Aplica-se quando:** há página de checkout própria.
- **Risco se faltar:** Magecart (script copia dados digitados).
- **Como verificar:** `curl -s $SITE/<checkout> | grep -oE '<script[^>]+src="https?://[^"]+'`; ler a CSP da página.
- **OK quando:** só scripts próprios, do gateway e do captcha.
- **Referência:** [checkout-e-webhook.md#1-escopo-pci](checkout-e-webhook.md#1-escopo-pci).

### SEC-PAG-08 — Portal do gateway com MFA em todos e login nominal
- **Aplica-se quando:** há portal web do gateway/adquirente.
- **Risco se faltar:** invasor muda a chave Pix e desvia o recebimento.
- **Como verificar:** pedir ao responsável a lista de usuários/perfis e o estado do 2FA de cada um (o agente não acessa o portal).
- **OK quando:** 2FA em todos, sem conta compartilhada, perfis mínimos, revisão periódica.
- **Referência:** [portal-do-gateway.md#3-checklist-de-configuração-antes-do-go-live](portal-do-gateway.md#3-checklist-de-configuração-antes-do-go-live) · PCI DSS 8.4.1.

### SEC-PAG-09 — Alteração de dado bancário confirmada fora de banda e conciliação diária
- **Aplica-se quando:** há recebimento por gateway.
- **Risco se faltar:** desvio só é descoberto quando o dinheiro já sumiu.
- **Como verificar:** perguntar/ler o procedimento e a rotina de conciliação.
- **OK quando:** procedimento escrito + conciliação diária ativa.
- **Referência:** [portal-do-gateway.md#3-checklist-de-configuração-antes-do-go-live](portal-do-gateway.md#3-checklist-de-configuração-antes-do-go-live).

### SEC-PAG-10 — Aprovação dupla em reembolso manual de alto valor
- **Aplica-se quando:** existe reembolso/emissão manual.
- **Risco se faltar:** um único operador (ou conta comprometida) devolve dinheiro à vontade.
- **Como verificar:** ler o fluxo de reembolso e onde mora a aprovação.
- **OK quando:** segunda aprovação acima de um valor (aqui ou no sistema consumidor), com log.
- **Referência:** [checkout-e-webhook.md#4-estados-e-atomicidade](checkout-e-webhook.md#4-estados-e-atomicidade) · ASVS V2.3.5.
