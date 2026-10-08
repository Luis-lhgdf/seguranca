# Checklist — Operação, incidentes e pessoas (OPS)

> **Revisado em:** 2026-10-07. Variáveis e regras em [`AGENTS.md`](../../AGENTS.md). Itens daqui dependem em geral de **perguntar** ao responsável: registrar a resposta como evidência ("informado por <pessoa> em <data>").

### SEC-OPS-01 — Runbook de incidente escrito
- **Aplica-se quando:** sistema em produção.
- **Risco se faltar:** no dia do vazamento, ninguém sabe quem avisar nem o prazo legal.
- **Como verificar:** procurar documento com contatos, contenção, avaliação, comunicação (ANPD/titulares) e recuperação.
- **OK quando:** existe, está atualizado e cita o prazo de comunicação.
- **Referência:** [incidentes-e-pessoas.md#1-plano-de-resposta-a-incidente-runbook](incidentes-e-pessoas.md#1-plano-de-resposta-a-incidente-runbook).

### SEC-OPS-02 — MFA nas contas externas do perímetro
- **Aplica-se quando:** sempre.
- **Risco se faltar:** invadir o e-mail, o domínio ou o GitHub dá controle do sistema sem tocar no código.
- **Como verificar:** listar as contas da seção 2 que o projeto usa e perguntar o estado de MFA de cada uma.
- **OK quando:** MFA em todas, com dono definido.
- **Referência:** [incidentes-e-pessoas.md#2-contas-satélites-fora-do-repositório-mas-no-perímetro](incidentes-e-pessoas.md#2-contas-satélites-fora-do-repositório-mas-no-perímetro).

### SEC-OPS-03 — Revisão periódica de acessos
- **Aplica-se quando:** mais de uma pessoa já teve acesso (painel, VPS, GitHub, provedores).
- **Risco se faltar:** ex-colaborador ou fornecedor mantém acesso.
- **Como verificar:** comparar listas de usuários (painel, `authorized_keys`, GitHub, provedores) com quem trabalha hoje.
- **OK quando:** só pessoas atuais, logins nominais.
- **Referência:** [incidentes-e-pessoas.md#2-contas-satélites-fora-do-repositório-mas-no-perímetro](incidentes-e-pessoas.md#2-contas-satélites-fora-do-repositório-mas-no-perímetro).

### SEC-OPS-04 — Procedimento contra phishing/BEC
- **Aplica-se quando:** há pagamentos, dados bancários ou atendimento ao cliente.
- **Risco se faltar:** um e-mail falso muda para onde vai o dinheiro.
- **Como verificar:** perguntar se há dupla verificação fora de banda e combinado público do que a empresa não pede.
- **OK quando:** procedimento definido e comunicado.
- **Referência:** [incidentes-e-pessoas.md#3-pessoas](incidentes-e-pessoas.md#3-pessoas).

### SEC-OPS-05 — Riscos aceitos e decisões registrados
- **Aplica-se quando:** sempre.
- **Risco se faltar:** pendência conhecida vira esquecimento.
- **Como verificar:** procurar registro de decisões/pendências de segurança com data e responsável.
- **OK quando:** cada desvio consciente está escrito, assinado e com data de reavaliação.
- **Referência:** [incidentes-e-pessoas.md#4-processo-de-desenvolvimento](incidentes-e-pessoas.md#4-processo-de-desenvolvimento).
