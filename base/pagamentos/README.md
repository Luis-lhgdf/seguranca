# Pagamentos

> **Revisado em:** 2026-10-07 · **Origem:** conteúdo compilado de fontes públicas (OWASP, ASVS, NIST, CWE, documentação oficial, avisos de CVE e artigos técnicos) — ver [referências](referencias.md).

**Cobre:** escopo PCI e checkout hospedado, valor recalculado, webhook (assinatura, revalidação,
idempotência), estados/atomicidade, card testing com limite em degraus, portal do gateway (BEC).
**Aplica-se quando:** o projeto processa pagamento ou recebe confirmação de pagamento.
**N/A quando** não há checkout, cobrança nem gateway (ex.: site institucional cuja venda acontece
fora do sistema) — registrar o motivo.

| Arquivo | Conteúdo |
|---|---|
| [checkout-e-webhook.md](checkout-e-webhook.md) | PCI, valor, webhook, estados, comunicação |
| [card-testing.md](card-testing.md) | ataque, defesas, degraus por pedido/conta/IP |
| [portal-do-gateway.md](portal-do-gateway.md) | BEC, Pix × cartão, configuração do portal |
| [referencias.md](referencias.md) | fontes oficiais e mapeamento Top 10 / ASVS / WSTG |
| [checklist.md](checklist.md) | itens `SEC-PAG-*` (com nível ASVS e mapeamento) |
