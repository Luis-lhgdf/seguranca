# Índice dos checklists (ordem de execução)

> **Revisado em:** 2026-10-08. Cada tema tem o seu `checklist.md` dentro de `base/<tema>/`.
> O agente percorre na ordem abaixo, depois das etapas 1 a 3 do [`AGENTS.md`](../AGENTS.md).

Referências cruzadas de cada item (OWASP Top 10:2025, ASVS 5.0 com nível L1/L2/L3, WSTG v4.2 e
API Security Top 10:2023) e índices reversos: [`mapeamentos.md`](mapeamentos.md).

| # | Tema | Prefixo | Itens | Aplica-se quando (resumo) | Checklist |
|---|---|---|---|---|---|
| 1 | Dependências e versões | `SEC-DEP` | 11 | sempre (alimenta a etapa 2) | [base/dependencias/checklist.md](../base/dependencias/checklist.md) |
| 2 | Segredos e configuração | `SEC-SEG` | 11 | sempre | [base/segredos/checklist.md](../base/segredos/checklist.md) |
| 3 | Autenticação, cadastro, recuperação | `SEC-AUTH` | 29 | há login | [base/autenticacao/checklist.md](../base/autenticacao/checklist.md) |
| 4 | Sessão e tokens | `SEC-SESS` | 10 | há área autenticada | [base/sessao/checklist.md](../base/sessao/checklist.md) |
| 5 | API e endpoints | `SEC-API` | 15 | há backend | [base/api/checklist.md](../base/api/checklist.md) |
| 6 | Upload e mídia | `SEC-UPL` | 11 | aceita arquivo | [base/upload/checklist.md](../base/upload/checklist.md) |
| 7 | Cabeçalhos, CSP e XSS | `SEC-NAV` | 12 | serve HTML | [base/headers/checklist.md](../base/headers/checklist.md) |
| 8 | Banco de dados | `SEC-BD` | 11 | há banco | [base/banco/checklist.md](../base/banco/checklist.md) |
| 9 | Pagamentos | `SEC-PAG` | 10 | processa pagamento | [base/pagamentos/checklist.md](../base/pagamentos/checklist.md) |
| 10 | Mensageria (WhatsApp/SMS/e-mail) | `SEC-MSG` | 11 | backend envia mensagem | [base/mensageria/checklist.md](../base/mensageria/checklist.md) |
| 11 | Rate limit, carga e abuso | `SEC-RL` | 10 | rota pública ou login | [base/rate-limit/checklist.md](../base/rate-limit/checklist.md) |
| 12 | Captcha | `SEC-CAP` | 8 | formulário público humano | [base/captcha/checklist.md](../base/captcha/checklist.md) |
| 13 | Infraestrutura de VPS | `SEC-VPS` | 16 | servidor próprio | [base/infra-vps/checklist.md](../base/infra-vps/checklist.md) |
| 14 | Nginx e TLS | `SEC-WEB` | 9 | proxy reverso próprio / HTTPS | [base/nginx-tls/checklist.md](../base/nginx-tls/checklist.md) |
| 15 | Cópias de segurança | `SEC-BKP` | 7 | dado persistente | [base/copias-de-seguranca/checklist.md](../base/copias-de-seguranca/checklist.md) |
| 16 | Logs, auditoria, monitoramento | `SEC-LOG` | 9 | produção | [base/logs/checklist.md](../base/logs/checklist.md) |
| 17 | Privacidade, LGPD, cookies | `SEC-LGPD` | 7 | dado pessoal | [base/privacidade/checklist.md](../base/privacidade/checklist.md) |
| 18 | Operação, incidentes, pessoas | `SEC-OPS` | 5 | produção | [base/operacao/checklist.md](../base/operacao/checklist.md) |
| | **Total** | | **202** | | |

`base/fundamentos/` não tem checklist: é contexto (princípios, catálogo V01–V24, golpes A01–A11,
ASVS). Seus itens estão distribuídos nos temas acima.

## Formato de cada item

```
### SEC-<AREA>-<NN> — <título curto>
- **Aplica-se quando:** <condição objetiva>
- **Risco se faltar:** <uma frase leiga>
- **Como verificar:** <passos/comandos concretos>
- **OK quando:** <critério objetivo>
- **Referência:** <arquivo.md#seção, OWASP/ASVS id>
- **Mapeamento:** nível L<n> · Top 10 Axx:2025 · ASVS Vx.y.z (L<n>) · WSTG-<CAT>-NN · APIn:2023
```

A linha **Mapeamento** traz o menor nível ASVS entre os requisitos citados (para filtrar o checklist
por nível) e as referências oficiais; partes sem correspondência são omitidas ou marcadas `—`. Ao
criar ou mudar um item, atualize a linha e a tabela em [`mapeamentos.md`](mapeamentos.md).

IDs são estáveis: ao remover um item, não reaproveite o número; ao adicionar, use o próximo livre.
