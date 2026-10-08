# Relatório de segurança — <projeto> — <AAAA-MM-DD>

> Gerado seguindo o [`AGENTS.md`](../AGENTS.md). Salvar como `relatorios/<projeto>/<AAAA-MM-DD>.md`
> (pasta ignorada pelo Git: o relatório descreve infraestrutura real e fica só local).
> Nenhum segredo ou dado pessoal sem máscara neste arquivo.

- **Auditor:** <agente/modelo> · **Solicitado por:** <responsável>
- **Repositório:** `<caminho ou URL>` · **Commit:** `<hash>`
- **Ambientes testados:** <local / teste / produção (só leitura)>
- **Autorizações recebidas:** <ex.: "pode rodar testssl e ssh-audit em produção" — ou "nenhuma além de leitura">
- **Relatório anterior:** <link ou "primeiro">

## 1. Cenário atual

- **O que é:** <descrição curta>
- **Em produção:** <URL, desde quando> · **Só em desenvolvimento:** <...>
- **Usuários:** <público, clientes logados (quantos), operadores do painel (quantos)>
- **Dados tratados:** <pessoais / sensíveis (saúde, financeiro, imagens)> · **Responsável LGPD:** <...>
- **Stack:** <linguagens, frameworks, banco, hospedagem, CDN>
- **Nível ASVS-alvo:** L2 · L3 em: <fluxos>

### Perfil de contexto

| Pergunta | Resposta | Evidência |
|---|---|---|
| Login (cliente/admin/social)? | | |
| Cadastro self-service / esqueci a senha / telefone 2º fator? | | |
| API pública de escrita / integrações / saída com URL externa? | | |
| Upload / mídia sensível / mídia privada? | | |
| Pagamento / webhook / portal de gateway? | | |
| Envio de e-mail/SMS/WhatsApp pelo backend? | | |
| Banco (tipo, autogerenciado/Docker/gerenciado)? | | |
| VPS própria / Docker / Nginx / CDN-WAF? | | |
| Backup sob nossa responsabilidade? | | |
| CI/CD (onde roda o build)? | | |
| Analytics / cookies de terceiros? | | |

## 2. Versões verificadas em <AAAA-MM-DD>

| Componente | Versão em uso (fonte) | Atual estável | Fim de suporte | CVEs/avisos para a versão em uso | Recomendação |
|---|---|---|---|---|---|
| SO | | | | | manter / subir / voltar — motivo + link |
| Linguagem/runtime | | | | | |
| Framework backend | | | | | |
| Framework front | | | | | |
| Bibliotecas críticas (auth, crypto, imagem, driver) | | | | | |
| Banco | | | | | |
| Nginx / proxy | | | | | |
| Imagens Docker / Actions | | | | | |

Saídas resumidas: `npm audit`: <...> · `pip-audit`: <...> · `apt list --upgradable`: <...>

## 3. Resumo por status

| Tema | OK | FALHA | PARCIAL | N/A | NÃO TESTÁVEL |
|---|---|---|---|---|---|
| DEP | | | | | |
| SEG | | | | | |
| AUTH | | | | | |
| SESS | | | | | |
| API | | | | | |
| UPL | | | | | |
| NAV | | | | | |
| BD | | | | | |
| PAG | | | | | |
| MSG | | | | | |
| RL | | | | | |
| CAP | | | | | |
| VPS | | | | | |
| WEB | | | | | |
| BKP | | | | | |
| LOG | | | | | |
| LGPD | | | | | |
| OPS | | | | | |
| **Total** | | | | | |

## 4. Achados (FALHA e PARCIAL)

### <SEC-XXX-NN> — <título> — <FALHA|PARCIAL> — severidade <crítica|alta|média|baixa>
- **O que foi verificado:** <comando/arquivo>
- **Evidência:** `<arquivo:linha>` ou saída resumida (mascarada)
- **Impacto no contexto deste projeto:** <...>
- **Correção proposta:** <...>

(repetir por achado; incluir também achados extras não cobertos pela base)

## 5. Correções priorizadas

| Prioridade | Itens | O que fazer | Esforço | Como validar (teste que deve reprovar antes) |
|---|---|---|---|---|
| P0 | | | | |
| P1 | | | | |
| P2 | | | | |

## 6. Itens OK (evidência resumida)

| Item | Evidência |
|---|---|
| | |

## 7. Itens N/A (motivo)

| Item | Motivo |
|---|---|
| | |

## 8. Itens NÃO TESTÁVEIS (o que falta)

| Item | O que seria necessário |
|---|---|
| | |

## 9. Sugestões para a base de conhecimento

<técnicas, armadilhas ou números medidos que valem para outros projetos>
