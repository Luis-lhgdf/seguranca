# Mensageria (WhatsApp, SMS, e-mail)

> **Revisado em:** 2026-10-07 · **Origem:** conteúdo compilado de fontes públicas (OWASP, ASVS, NIST, CWE, documentação oficial, avisos de CVE e artigos técnicos) — ver [referências](referencias.md).

**Cobre:** toll fraud, ordem de contagem com vários limites, dimensões de limite (conta, IP,
destino, país, global, conversão), custo por canal, registro e conciliação de gasto, alertas,
SPF/DKIM/DMARC.
**Aplica-se quando:** o backend envia OTP, código ou mensagem transacional. **N/A quando** o
contato é só link `wa.me`/`mailto:` aberto pelo visitante (nada sai do servidor).

| Arquivo | Conteúdo |
|---|---|
| [limites-e-toll-fraud.md](limites-e-toll-fraud.md) | risco, ordem da contagem, dimensões, regras de envio |
| [custo-e-entregabilidade.md](custo-e-entregabilidade.md) | preços, o que registrar, alertas, SPF/DKIM/DMARC |
| [referencias.md](referencias.md) | fontes oficiais |
| [checklist.md](checklist.md) | itens `SEC-MSG-*` |

Recuperação de senha e telefone: [autenticacao](../autenticacao/README.md).
