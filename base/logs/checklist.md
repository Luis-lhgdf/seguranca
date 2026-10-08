# Checklist — Logs, auditoria e monitoramento (LOG)

> **Revisado em:** 2026-10-07. Variáveis e regras em [`AGENTS.md`](../../AGENTS.md). Ao citar evidência de log, **mascarar** IP, e-mail e qualquer dado pessoal.

### SEC-LOG-01 — Eventos de autenticação auditados
- **Aplica-se quando:** há login.
- **Risco se faltar:** tentativa de invasão não deixa rastro.
- **Como verificar:** `grep -rn "audit" <módulo de auth>`; em teste, falhar login e conferir o registro.
- **OK quando:** sucesso, falha, lockout, logout e reuso de refresh registrados.
- **Referência:** [trilha-de-auditoria.md#1-o-que-registrar-asvs-v1621-v1631-v1632](trilha-de-auditoria.md#1-o-que-registrar-asvs-v1621-v1631-v1632) · ASVS V16.3.1.

### SEC-LOG-02 — Ações sobre dado sensível auditadas, inclusive leitura e delete
- **Aplica-se quando:** há dado pessoal/sensível.
- **Risco se faltar:** impossível responder "quem viu/apagou" numa fiscalização LGPD.
- **Como verificar:** listar rotas que tocam dado sensível e conferir chamada de auditoria em cada uma (create/update/delete/download/exibição).
- **OK quando:** cobertura completa.
- **Referência:** [trilha-de-auditoria.md#1-o-que-registrar-asvs-v1621-v1631-v1632](trilha-de-auditoria.md#1-o-que-registrar-asvs-v1621-v1631-v1632).

### SEC-LOG-03 — Mudança de configuração com antes/depois
- **Aplica-se quando:** há configurações editáveis no painel.
- **Risco se faltar:** não se sabe quem desligou um controle nem para qual valor.
- **Como verificar:** ler o registro de `settings.update`; flags de compliance restritas a superuser?
- **OK quando:** valor anterior e novo registrados; flags críticas restritas.
- **Referência:** [trilha-de-auditoria.md#1-o-que-registrar-asvs-v1621-v1631-v1632](trilha-de-auditoria.md#1-o-que-registrar-asvs-v1621-v1631-v1632).

### SEC-LOG-04 — Auditoria gravada na mesma transação
- **Aplica-se quando:** há trilha em banco.
- **Risco se faltar:** log de ação que não aconteceu, ou ação sem log.
- **Como verificar:** ler a função de registro (adiciona na sessão, sem commit próprio) e a ordem nas rotas.
- **OK quando:** registro antes do commit da ação.
- **Referência:** [trilha-de-auditoria.md#2-como-registrar](trilha-de-auditoria.md#2-como-registrar).

### SEC-LOG-05 — Nada de segredo ou vínculo sensível em log
- **Aplica-se quando:** sempre.
- **Risco se faltar:** o log vira o vazamento.
- **Como verificar:** `grep -rnE "log(ger)?\.(info|debug|warning|error)\(.*(password|senha|token|secret|otp|codigo|cpf)" $REPO`; conferir scrubbing do Sentry.
- **OK quando:** nenhum segredo/PII sensível logado.
- **Referência:** [trilha-de-auditoria.md#3-o-que-não-registrar](trilha-de-auditoria.md#3-o-que-não-registrar).

### SEC-LOG-06 — Alertas saem do servidor e têm dono
- **Aplica-se quando:** produção.
- **Risco se faltar:** problema descoberto pelo cliente.
- **Como verificar:** perguntar/listar: uptime externo, Sentry, canal de alerta, quem recebe.
- **OK quando:** pelo menos disponibilidade + erros + disco com alerta externo e dono definido.
- **Referência:** [monitoramento-e-alerta.md#2-o-que-monitorar](monitoramento-e-alerta.md#2-o-que-monitorar).

### SEC-LOG-07 — Logs copiados para fora do servidor
- **Aplica-se quando:** produção.
- **Risco se faltar:** invasor apaga o rastro junto com o servidor.
- **Como verificar:** procurar envio remoto (journal-remote, Loki, serviço gerenciado).
- **OK quando:** logs de segurança com cópia externa e retenção definida.
- **Referência:** [monitoramento-e-alerta.md#3-detecção-de-ataque-lacunas-típicas](monitoramento-e-alerta.md#3-detecção-de-ataque-lacunas-típicas).

### SEC-LOG-08 — Detecção de volume anômalo
- **Aplica-se quando:** há acervo sensível ou rotas de abuso caro.
- **Risco se faltar:** raspagem ou ataque distribuído passam despercebidos.
- **Como verificar:** procurar jail/cron/painel que alerta por volume (downloads por IP, 401/429, envios).
- **OK quando:** existe critério de volume com alerta.
- **Referência:** [monitoramento-e-alerta.md#2-o-que-monitorar](monitoramento-e-alerta.md#2-o-que-monitorar).

### SEC-LOG-09 — Trilha protegida e com retenção
- **Aplica-se quando:** há trilha de auditoria.
- **Risco se faltar:** trilha adulterável ou crescendo para sempre com dado pessoal.
- **Como verificar:** quem lê (superuser?), se a app pode editar/apagar, se há expurgo agendado.
- **OK quando:** leitura restrita, append-only, prazo definido.
- **Referência:** [trilha-de-auditoria.md#4-retenção](trilha-de-auditoria.md#4-retenção).
