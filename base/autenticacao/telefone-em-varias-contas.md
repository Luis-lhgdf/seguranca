# Telefone como 2º fator: troca, número reciclado e o mesmo número em várias contas

> **Revisado em:** 2026-10-07 · **Origem:** conteúdo compilado de fontes públicas (OWASP, ASVS, NIST, CWE, documentação oficial, avisos de CVE e artigos técnicos) — ver [referências](referencias.md). Se a data estiver antiga (> 6 meses) ou o tema envolver versão/preço/CVE, confirme na fonte oficial antes de aplicar.

Aplica-se quando o celular é verificado e usado como canal de código (cadastro, login, step-up).

## 1. Trocar o número

- Trocar número **já verificado** exige **prova de posse do número atual** (código ao número atual antes de gravar o novo); o novo entra pendente. Rota genérica de perfil (`PUT /perfil`) **recusa** trocar número verificado (409). — ASVS 7.5.1; NIST: *"Setting or changing the pre-registered telephone number is considered to be the binding of a new authenticator"*.
- OWASP MFA CS: reautenticar com fator existente; não confiar só na sessão ativa; avisar fora de banda; considerar atraso/step-up em conta de alto valor.

## 2. O número muda de dono

- Brasil (Anatel Ato 12.712/2024): número liberado fica **≥ 6 meses** em quarentena. Pré-pago (≈70% das linhas) pode ser cancelado ~75 dias sem recarga → número pode chegar a outra pessoa **~9 meses** depois (estimativa; conferir o RGC vigente).
- Não há base pública brasileira de números reatribuídos (equivalente à FCC dos EUA) — a conta não fica sabendo.
- WhatsApp apaga conta inativa após ~120 dias; o novo dono que instala o WhatsApp recebe o código da conta antiga.
- NIST manda considerar *"device swap, SIM change, number porting"*; ASVS V6.6: ignorar isso em app L2 sensível é *"significant red flag"*.

## 3. O mesmo número verificado em várias contas

Achado típico em auditoria: nenhuma checagem; 3 contas com o mesmo número verificado; nenhuma avisada.

| Opção | Prós | Contras |
|---|---|---|
| **A. O último que prova fica** (Mercado Livre, Shopee) | um 2º fator por pessoa; reciclado se resolve; sinal vira **aviso** | DoS de quem clonou o número; celular de família vira pingue-pongue |
| B. Número único, recusa (Amazon, Uber) | simples | **enumera**; reciclado preso ao SAC; contra NIST (*"SHOULD NOT prevent"*) |
| C. Deixar como está | celular de família funciona | reciclado recebe código alheio; ninguém avisado |
| D. Limitar N contas por número e avisar (Google; NIST *"MAY"*) | família funciona; corta abuso em massa | reciclado continua recebendo código |

Nenhuma norma exige número único; o que exigem é o **ciclo de vida**: vincular = autenticar no nível
da conta; comprometido → invalidar (*"consequences of not invalidating... more significant than the
denial-of-service"*); avisar por canal independente.

**Padrão recomendado: A, com travas:**
- índice único **parcial** em `telefone` onde `telefone_verificado` (regra no banco);
- na **mesma transação** da verificação, o número sai da conta antiga (`SELECT ... FOR UPDATE`);
- 🔴 a conta antiga vai para estado **"celular desvinculado"**, **não** "pendente": o login com senha
  pede código no **e-mail confirmado** antes de vincular número novo; sem e-mail confirmado → SAC;
  `PUT /perfil` não troca número nesse estado. *(Achado: no estado "pendente", quem tinha só a senha
  entrava sem 2º fator e cadastrava o próprio número.)*
- aviso à conta antiga: e-mail de segurança (se confirmado) **e** faixa na tela no próximo login;
- registro de auditoria (conta antiga, nova, data) **sem o número no log**;
- teto de trocas de conta por número por dia;
- **trava com voucher/pedido ativo** (como a Shopee): mensagem neutra a quem tentou, aviso à dona;
- nunca recusar no cadastro com mensagem diferente (sem enumeração).

## 4. Limites de envio por número

O OTP de cadastro é a rota em que **quem pede escolhe o destino** → limitar por número de destino
(não só por conta). Ver [mensageria](../mensageria/README.md).
