# Checklist — Autenticação, cadastro e recuperação (AUTH)

> **Revisado em:** 2026-10-07. Variáveis (`$SITE`, `$API`, `$REPO`, `$VPS`) e regras de execução em [`AGENTS.md`](../../AGENTS.md). Testes que escrevem dados (cadastro, login com erro, reset) **só em ambiente local/de teste**.

### SEC-AUTH-01 — Senha guardada com Argon2id
- **Aplica-se quando:** há login com senha.
- **Risco se faltar:** se o banco vazar, as senhas são descobertas e reaproveitadas em outros sites.
- **Como verificar:** `grep -rniE "argon2|bcrypt|pbkdf2|scrypt|md5|sha1|sha256\(" $REPO --include=*.{py,ts,js}`; em base de teste, `SELECT senha_hash FROM <tabela> LIMIT 1` deve começar com `$argon2id$`.
- **OK quando:** Argon2id (bcrypt só em legado, ciente do limite de 72 bytes); nenhum hash rápido nem texto puro.
- **Referência:** [senhas-hash-e-pepper.md#1-por-que-argon2id-e-não-bcrypt](senhas-hash-e-pepper.md#1-por-que-argon2id-e-não-bcrypt) · ASVS V11.4.2, V6.
- **Mapeamento:** nível L2 · Top 10 A04:2025, A07:2025 · ASVS V11.4.2 (L2).

### SEC-AUTH-02 — Parâmetros do Argon2id ≥ mínimo OWASP e medidos no servidor
- **Aplica-se quando:** SEC-AUTH-01 se aplica.
- **Risco se faltar:** hash barato demais facilita ataque offline; caro demais derruba o servidor em pico.
- **Como verificar:** ler os parâmetros no código ou na string PHC (`m=…,t=…,p=…`); pedir/ler medição de latência e memória na VPS.
- **OK quando:** `m≥19456,t≥2,p≥1` (ou linha equivalente da tabela) e há número medido em produção.
- **Referência:** [senhas-hash-e-pepper.md#2-parâmetros-do-argon2id](senhas-hash-e-pepper.md#2-parâmetros-do-argon2id).
- **Mapeamento:** nível L2 · Top 10 A04:2025 · ASVS V11.4.2 (L2).

### SEC-AUTH-03 — Pepper aplicado antes do hash (HMAC) e guardado fora do banco
- **Aplica-se quando:** há login com senha (recomendado; obrigatório se o banco guarda dado sensível).
- **Risco se faltar:** um dump do banco basta para atacar as senhas offline.
- **Como verificar:** localizar a função de hash; conferir `argon2id(hmac_sha256(PEPPER, senha))`; conferir que o pepper vem do ambiente/arquivo de segredo, não de tabela; conferir validador que recusa placeholder/curto (< 32).
- **OK quando:** ordem pré-hash HMAC, pepper fora do banco, app não sobe sem pepper forte.
- **Referência:** [senhas-hash-e-pepper.md#41-a-ordem-correta-pré-hash-com-hmac](senhas-hash-e-pepper.md#41-a-ordem-correta-pré-hash-com-hmac).
- **Mapeamento:** nível L2 · Top 10 A04:2025 · ASVS V11.4.2 (L2), V13.3.1 (L2).

### SEC-AUTH-04 — Rehash automático no login
- **Aplica-se quando:** SEC-AUTH-01 se aplica.
- **Risco se faltar:** senhas antigas ficam para sempre com custo antigo.
- **Como verificar:** `grep -rn "needs_rehash\|check_needs_rehash" $REPO`; confirmar que o novo hash é persistido.
- **OK quando:** login bem-sucedido regrava hash com parâmetros abaixo do atual.
- **Referência:** [senhas-hash-e-pepper.md#3-rehash-automático](senhas-hash-e-pepper.md#3-rehash-automático).
- **Mapeamento:** nível L2 · Top 10 A04:2025 · ASVS V11.2.2 (L2).

### SEC-AUTH-05 — Plano do pepper escrito (backup separado, rotação, versão)
- **Aplica-se quando:** há pepper.
- **Risco se faltar:** perder ou trocar o pepper tranca todo mundo fora, sem volta.
- **Como verificar:** procurar no repositório/docs o procedimento de rotação e onde fica o backup do pepper; conferir se existe `pepper_versao` ou justificativa escrita para não ter.
- **OK quando:** procedimento escrito; backup do pepper em local diferente do backup do banco.
- **Referência:** [senhas-hash-e-pepper.md#42-o-custo-que-precisa-estar-escrito-antes-do-primeiro-cadastro](senhas-hash-e-pepper.md#42-o-custo-que-precisa-estar-escrito-antes-do-primeiro-cadastro).
- **Mapeamento:** nível L2 · Top 10 A04:2025 · ASVS V11.1.1 (L2).

### SEC-AUTH-06 — Testes automatizados de salt e de pepper
- **Aplica-se quando:** há pepper.
- **Risco se faltar:** uma refatoração remove o pepper e nada acusa.
- **Como verificar:** procurar testes "mesma senha → hashes diferentes" e "pepper errado não confere"; rodar a suíte localmente.
- **OK quando:** os dois testes existem e passam.
- **Referência:** [senhas-hash-e-pepper.md#8-testes-mínimos-baratos-e-de-alto-valor](senhas-hash-e-pepper.md#8-testes-mínimos-baratos-e-de-alto-valor).
- **Mapeamento:** nível L2 · Top 10 A04:2025 · ASVS V11.4.2 (L2).

### SEC-AUTH-07 — Login sem enumeração (mensagem e tempo iguais)
- **Aplica-se quando:** há login.
- **Risco se faltar:** o atacante descobre quais e-mails têm conta.
- **Como verificar:** ler o fluxo: usuário inexistente, bloqueado e **inativo** passam por `dummy_verify`; em ambiente de teste, medir `curl -w '%{time_total}'` para e-mail inexistente × existente com senha errada (10 amostras cada).
- **OK quando:** mesma mensagem e tempos estatisticamente equivalentes em todos os ramos.
- **Referência:** [senhas-hash-e-pepper.md#5-fluxo-de-login-seguro](senhas-hash-e-pepper.md#5-fluxo-de-login-seguro) · ASVS V6.3.8.
- **Mapeamento:** nível L3 · Top 10 A07:2025 · ASVS V6.3.8 (L3) · WSTG-IDNT-04.

### SEC-AUTH-08 — Rate limit no login na borda e na aplicação
- **Aplica-se quando:** há login.
- **Risco se faltar:** força bruta e credential stuffing ilimitados.
- **Como verificar:** `ssh $VPS 'sudo nginx -T | grep -nE "limit_req(_zone)?"'`; grep do decorator/middleware no app; em teste, 10 logins errados em 1 min → 429.
- **OK quando:** limite dedicado no login na borda **e** no app (ou storage compartilhado).
- **Referência:** [login-e-mfa.md#1-camadas-contra-força-bruta-e-credential-stuffing](login-e-mfa.md#1-camadas-contra-força-bruta-e-credential-stuffing).
- **Mapeamento:** nível L1 · Top 10 A07:2025 · ASVS V6.1.1 (L1), V6.3.1 (L1) · WSTG-ATHN-03 · API4:2023.

### SEC-AUTH-09 — Lockout por conta, curto e persistido
- **Aplica-se quando:** há login.
- **Risco se faltar:** ataque lento por muitos IPs passa; ou o lockout vira DoS longo do dono.
- **Como verificar:** ler contador de falhas na conta, teto e duração; conferir que o contador é gravado antes do 401.
- **OK quando:** contador na conta, lockout temporário curto (ex.: 10 falhas/15 min), sem escalonamento.
- **Referência:** [senhas-hash-e-pepper.md#5-fluxo-de-login-seguro](senhas-hash-e-pepper.md#5-fluxo-de-login-seguro).
- **Mapeamento:** nível L1 · Top 10 A07:2025 · ASVS V6.3.1 (L1) · WSTG-ATHN-03.

### SEC-AUTH-10 — MFA em toda conta administrativa
- **Aplica-se quando:** há painel/admin ou conta com acesso a dado sensível ou dinheiro.
- **Risco se faltar:** um phishing ou senha reaproveitada entrega o sistema inteiro.
- **Como verificar:** `grep -rniE "totp|otp|mfa|2fa|two_factor|webauthn|passkey" $REPO`; tentar login admin só com senha em ambiente de teste.
- **OK quando:** login admin exige 2º fator (TOTP/WebAuthn), com códigos de recuperação.
- **Referência:** [login-e-mfa.md#2-mfa](login-e-mfa.md#2-mfa) · PCI DSS 8.4.1.
- **Mapeamento:** nível L2 · Top 10 A07:2025 · ASVS V6.3.3 (L2).

### SEC-AUTH-11 — Step-up em aparelho novo / sinais de risco
- **Aplica-se quando:** contas de usuário guardam valor (voucher, saldo) ou dado sensível.
- **Risco se faltar:** senha vazada de outro site basta para tomar a conta.
- **Como verificar:** ler o fluxo de login: existe cookie de aparelho confiável/gatilho que pede 2º fator?
- **OK quando:** aparelho novo (ou N erros) pede 2º fator; troca de senha esquece aparelhos.
- **Referência:** [login-e-mfa.md#3-step-up-login-adaptativo](login-e-mfa.md#3-step-up-login-adaptativo).
- **Mapeamento:** nível L3 · Top 10 A07:2025 · ASVS V7.5.3 (L3), V8.2.4 (L3).

### SEC-AUTH-12 — Reautenticação para mudar senha, e-mail, telefone ou fator
- **Aplica-se quando:** há autoatendimento dessas mudanças (ou superuser alterando credenciais).
- **Risco se faltar:** uma sessão roubada vira tomada permanente da conta.
- **Como verificar:** ler as rotas de alteração; conferir exigência de senha atual ou código no fator existente.
- **OK quando:** toda mudança de credencial exige prova recente.
- **Referência:** [login-e-mfa.md#4-reautenticação-e-notificação](login-e-mfa.md#4-reautenticação-e-notificação) · ASVS V7.5.1.
- **Mapeamento:** nível L2 · Top 10 A07:2025 · ASVS V7.5.1 (L2) · WSTG-ATHN-09.

### SEC-AUTH-13 — Aviso ao titular após mudança de credencial
- **Aplica-se quando:** há conta com credencial alterável.
- **Risco se faltar:** a vítima não fica sabendo que perdeu a conta.
- **Como verificar:** procurar envio de aviso em troca de senha, celular, aparelho novo, recuperação.
- **OK quando:** aviso por canal independente com instrução "não fui eu".
- **Referência:** [login-e-mfa.md#4-reautenticação-e-notificação](login-e-mfa.md#4-reautenticação-e-notificação) · ASVS V6.3.7.
- **Mapeamento:** nível L3 · Top 10 A07:2025 · ASVS V6.3.7 (L3).

### SEC-AUTH-14 — Política de senha (tamanho mínimo/máximo, senha vazada)
- **Aplica-se quando:** há criação/troca de senha.
- **Risco se faltar:** senhas fracas ou payload gigante no hash.
- **Como verificar:** ler o schema (`min_length`, `max_length`); procurar checagem HIBP.
- **OK quando:** mínimo ≥ 12 (admin) / ≥ 8 (cliente), máximo ~128, sem troca periódica forçada; checagem de vazada recomendada.
- **Referência:** [senhas-hash-e-pepper.md#6-política-de-senha-nist-sp-800-63b](senhas-hash-e-pepper.md#6-política-de-senha-nist-sp-800-63b).
- **Mapeamento:** nível L1 · Top 10 A07:2025 · ASVS V6.2.1 (L1), V6.2.9 (L2), V6.2.12 (L2) · WSTG-ATHN-07.

### SEC-AUTH-15 — Bootstrap do primeiro admin fechado
- **Aplica-se quando:** existe rota/script de setup inicial.
- **Risco se faltar:** qualquer um cria o primeiro admin em produção.
- **Como verificar:** `curl -s -o /dev/null -w '%{http_code}' -X POST $API/<rota-setup>` (sem corpo válido) → 403/409; ler o código; checar presença (não o valor) de `SETUP_TOKEN` no `.env`: `ssh $VPS 'grep -c "^SETUP_TOKEN=.\+" <caminho>/.env'`.
- **OK quando:** fail-closed em produção, 409 após o 1º usuário, token vazio depois do uso.
- **Referência:** [login-e-mfa.md#5-painel-de-operador-único](login-e-mfa.md#5-painel-de-operador-único).
- **Mapeamento:** nível L1 · Top 10 A07:2025 · ASVS V6.3.2 (L1), V6.4.1 (L1) · WSTG-ATHN-02.

### SEC-AUTH-16 — Acesso ao painel restrito por origem (recomendado)
- **Aplica-se quando:** o painel tem poucos operadores fixos.
- **Risco se faltar:** o login do admin fica exposto ao mundo todo.
- **Como verificar:** `ssh $VPS 'sudo nginx -T | grep -nA5 "location.*admin"'` procurando `allow/deny` ou auth extra.
- **OK quando:** allowlist de IP/VPN ou justificativa registrada.
- **Referência:** [login-e-mfa.md#5-painel-de-operador-único](login-e-mfa.md#5-painel-de-operador-único).
- **Mapeamento:** nível L3 · Top 10 A01:2025 · ASVS V8.4.2 (L3) · WSTG-CONF-05.

### SEC-AUTH-17 — Login social sem auto-vínculo e com `email_verified` confiável
- **Aplica-se quando:** há OAuth/OIDC.
- **Risco se faltar:** alguém entra na conta de outra pessoa criando conta no provedor com o mesmo e-mail.
- **Como verificar:** ler o callback: vincula por e-mail? aceita `email_verified` do Google sem `@gmail.com`/`hd`? assume Facebook verificado?
- **OK quando:** sem vínculo automático por e-mail; `email_verified` só onde o provedor é autoritativo.
- **Referência:** [login-e-mfa.md#6-login-social-oauthoidc--se-houver](login-e-mfa.md#6-login-social-oauthoidc--se-houver).
- **Mapeamento:** nível L2 · Top 10 A07:2025 · ASVS V6.8.1 (L2), V10.5.2 (L2).

### SEC-AUTH-18 — Funções barradas até verificar e-mail/telefone
- **Aplica-se quando:** há cadastro self-service.
- **Risco se faltar:** contas falsas usam recursos gratuitos ou caros.
- **Como verificar:** listar rotas que exigem conta verificada × sessão pendente; testar agendar/usar cupom/comprar com conta não verificada (ambiente de teste).
- **OK quando:** a coluna de verificação de fato bloqueia as funções que causam dano.
- **Referência:** [cadastro-e-enumeracao.md#1-cadastro-em-massa-owasp-oat-019-account-creation](cadastro-e-enumeracao.md#1-cadastro-em-massa-owasp-oat-019-account-creation).
- **Mapeamento:** nível L1 · Top 10 A07:2025 · ASVS V2.3.1 (L1) · WSTG-IDNT-02.

### SEC-AUTH-19 — Cadastro e recuperação sem enumeração
- **Aplica-se quando:** há cadastro ou "esqueci a senha".
- **Risco se faltar:** revela quem é cliente (em saúde, perto de dado sensível).
- **Como verificar:** em teste, cadastrar e-mail/CPF/telefone já existente e comparar resposta e status com um novo.
- **OK quando:** resposta igual; o aviso vai por e-mail ao dono.
- **Referência:** [cadastro-e-enumeracao.md#3-enumeração](cadastro-e-enumeracao.md#3-enumeração) · ASVS V6.3.8.
- **Mapeamento:** nível L3 · Top 10 A07:2025 · ASVS V6.3.8 (L3) · WSTG-IDNT-04.

### SEC-AUTH-20 — Velocidade de cadastro limitada
- **Aplica-se quando:** há cadastro self-service.
- **Risco se faltar:** cadastro em massa (OAT-019).
- **Como verificar:** procurar limite de cadastros por IP (e ASN/dispositivo); captcha na rota.
- **OK quando:** limite por pelo menos IP + captcha; monitoramento de cadastros/hora.
- **Referência:** [cadastro-e-enumeracao.md#1-cadastro-em-massa-owasp-oat-019-account-creation](cadastro-e-enumeracao.md#1-cadastro-em-massa-owasp-oat-019-account-creation).
- **Mapeamento:** nível L1 · Top 10 A06:2025 · ASVS V2.4.1 (L2), V6.1.1 (L1) · WSTG-IDNT-02, WSTG-BUSL-05 · API6:2023.

### SEC-AUTH-21 — E-mail não verificado não prende o endereço do dono
- **Aplica-se quando:** cadastro aceita e-mail sem verificá-lo antes.
- **Risco se faltar:** alguém cadastra o e-mail de outra pessoa e ela nunca mais consegue usar.
- **Como verificar:** em teste, cadastrar com e-mail X sem verificar; tentar cadastrar de novo como "dono" de X.
- **OK quando:** existe caminho ("não fui eu", não reserva, aviso ao dono) que libera o endereço.
- **Referência:** [cadastro-e-enumeracao.md#2-e-mail-de-outra-pessoa-prendendo-o-endereço-sequestro](cadastro-e-enumeracao.md#2-e-mail-de-outra-pessoa-prendendo-o-endereço-sequestro).
- **Mapeamento:** Top 10 A07:2025 · sem requisito ASVS direto · WSTG-IDNT-02.

### SEC-AUTH-22 — Nenhuma conta de teste/seed em produção
- **Aplica-se quando:** sempre que há usuários em banco.
- **Risco se faltar:** senha conhecida dá acesso a produção.
- **Como verificar:** procurar seeds/scripts e se checam `ENV`; pedir ao responsável uma consulta de leitura em produção por e-mails de teste (`%test%`, `%example%`).
- **OK quando:** seed bloqueado em produção e consulta vazia.
- **Referência:** [cadastro-e-enumeracao.md#6-contas-de-teste](cadastro-e-enumeracao.md#6-contas-de-teste).
- **Mapeamento:** nível L1 · Top 10 A07:2025, A02:2025 · ASVS V6.3.2 (L1), V15.2.3 (L2) · WSTG-ATHN-02.

### SEC-AUTH-23 — Código de recuperação forte e de uso único
- **Aplica-se quando:** há "esqueci a senha".
- **Risco se faltar:** código adivinhável ou reutilizável.
- **Como verificar:** ler geração (CSPRNG, ≥ 6 dígitos), armazenamento (hash/HMAC), validade (≤ 10 min telefone, ≤ 24 h e-mail), teto de palpites contado antes de comparar, invalidação após uso.
- **OK quando:** todos os itens presentes.
- **Referência:** [recuperacao-de-senha.md#1-fluxo-de-referência](recuperacao-de-senha.md#1-fluxo-de-referência).
- **Mapeamento:** nível L2 · Top 10 A07:2025 · ASVS V6.5.1 (L2), V6.5.3 (L2), V6.5.5 (L2) · WSTG-ATHN-09.

### SEC-AUTH-24 — Palpites contados por conta, sobrevivendo ao código novo
- **Aplica-se quando:** há código de recuperação/verificação com reenvio.
- **Risco se faltar:** pedir código novo zera o limite e permite adivinhar sem fim.
- **Como verificar:** ler onde o contador de palpites é zerado; teste local: 5 códigos × 5 palpites.
- **OK quando:** contador por conta+finalidade com teto (≤ 100 consecutivos, NIST).
- **Referência:** [recuperacao-de-senha.md#3--palpites-acumulados-entre-códigos](recuperacao-de-senha.md#3--palpites-acumulados-entre-códigos).
- **Mapeamento:** nível L2 · Top 10 A07:2025 · ASVS V6.6.3 (L2) · WSTG-ATHN-09.

### SEC-AUTH-25 — Recuperação não contorna o 2º fator
- **Aplica-se quando:** há recuperação e há 2º fator.
- **Risco se faltar:** quem controla só o telefone (SIM swap) toma a conta.
- **Como verificar:** comparar o canal da recuperação com o canal do 2º fator do login.
- **OK quando:** recuperar exige fator diferente do usado no login (ou os dois).
- **Referência:** [recuperacao-de-senha.md#4-qual-canal-segurança--conveniência](recuperacao-de-senha.md#4-qual-canal-segurança--conveniência) · ASVS V6.4.3.
- **Mapeamento:** nível L2 · Top 10 A07:2025 · ASVS V6.4.3 (L2) · WSTG-ATHN-09.

### SEC-AUTH-26 — Autorização de senha nova fora da URL e sessões derrubadas
- **Aplica-se quando:** há recuperação ou troca de senha.
- **Risco se faltar:** token vaza em log/Referer; sessão do atacante continua viva.
- **Como verificar:** ler o fluxo pós-código (cookie httpOnly/Strict com path restrito ou equivalente); verificar revogação de todas as sessões ao trocar.
- **OK quando:** sem segredo em URL; todas as sessões e aparelhos revogados.
- **Referência:** [recuperacao-de-senha.md#1-fluxo-de-referência](recuperacao-de-senha.md#1-fluxo-de-referência).
- **Mapeamento:** nível L1 · Top 10 A07:2025 · ASVS V14.2.1 (L1), V7.4.3 (L2) · WSTG-ATHN-09.

### SEC-AUTH-27 — Link de e-mail (se houver) resistente a scanner e Referer
- **Aplica-se quando:** reset ou confirmação usa link com token.
- **Risco se faltar:** scanner de e-mail consome o token; token vaza por Referer; link envenenado via `Host`.
- **Como verificar:** GET do link não executa a ação (tela + POST); `Referrer-Policy: no-referrer` na página; URL montada de config, não do header `Host`.
- **OK quando:** os três itens atendidos.
- **Referência:** [recuperacao-de-senha.md#2-código-pin--link-com-token](recuperacao-de-senha.md#2-código-pin--link-com-token).
- **Mapeamento:** nível L2 · Top 10 A07:2025 · ASVS V6.5.1 (L2), V3.4.5 (L2) · WSTG-ATHN-09.

### SEC-AUTH-28 — Troca de telefone verificado prova posse do atual
- **Aplica-se quando:** telefone é verificado e usado como canal de código.
- **Risco se faltar:** sessão roubada troca o 2º fator.
- **Como verificar:** em teste, `PUT` de perfil trocando número verificado → 409; fluxo dedicado envia código ao número atual.
- **OK quando:** os dois comportamentos confirmados.
- **Referência:** [telefone-em-varias-contas.md#1-trocar-o-número](telefone-em-varias-contas.md#1-trocar-o-número).
- **Mapeamento:** nível L2 · Top 10 A07:2025 · ASVS V7.5.1 (L2), V6.6.1 (L2) · WSTG-ATHN-09.

### SEC-AUTH-29 — Política para o mesmo telefone em várias contas
- **Aplica-se quando:** telefone é 2º fator ou canal de login.
- **Risco se faltar:** número reciclado recebe código de conta alheia; ninguém é avisado.
- **Como verificar:** procurar índice único (parcial) em telefone verificado; ler o que acontece com a conta que perde o número (não pode virar "pendente" sem 2º fator).
- **OK quando:** política escolhida e escrita (A/B/C/D) e conta que perde o número não fica mais fraca.
- **Referência:** [telefone-em-varias-contas.md#3-o-mesmo-número-verificado-em-várias-contas](telefone-em-varias-contas.md#3-o-mesmo-número-verificado-em-várias-contas).
- **Mapeamento:** nível L2 · Top 10 A06:2025 · ASVS V6.6.1 (L2).
