# Recuperação de senha ("esqueci a senha")

> **Revisado em:** 2026-10-07 · **Origem:** conteúdo compilado de fontes públicas (OWASP, ASVS, NIST, CWE, documentação oficial, avisos de CVE e artigos técnicos) — ver [referências](referencias.md). Se a data estiver antiga (> 6 meses) ou o tema envolver versão/preço/CVE, confirme na fonte oficial antes de aplicar.

**N/A quando** não existe fluxo público de reset (ex.: painel de operador único — senha trocada só
por superuser autenticado; menos superfície). Custo de mensagem: ver [mensageria](../mensageria/README.md).

## 1. Fluxo de referência

| Passo | Controle |
|---|---|
| Pedir | captcha obrigatório (fail-closed); resposta **sempre igual**; trabalho roda **depois** da resposta (tempo igual com e sem conta) |
| Canal | só canal **verificado** recebe código de senha |
| Código | 6 dígitos CSPRNG · só o **HMAC** guardado (Redis) · **10 min** · **5 palpites** contados **antes** de comparar · uso único · comparação em tempo constante · reenvio após 60 s (o novo substitui o anterior) |
| Conferir | captcha · teto de conferências por IP (ex.: 30/h) · e-mail sem conta = "código inválido" |
| Senha nova | autorização de uso único, 10 min, em **cookie httpOnly `SameSite=Strict` com path restrito** (nunca na URL) · derruba **todas** as sessões · esquece aparelhos · aviso por e-mail |

## 2. Código (PIN) × link com token

| Critério | Código 6 dígitos | Link com token (≥ 64 bits) |
|---|---|---|
| Brute force | 10⁶: depende **só** dos limites | inviável (ASVS 6.6.3) |
| Vazamento | não passa por URL | token **na URL**: logs, histórico, `Referer` (exige `no-referrer`) |
| Scanner de e-mail (Safe Links) | não afeta | abre o link antes da pessoa: GET **não pode** consumir; exige tela com POST |
| Phishing | "me passa o código" | link falso parecido |
| Cruzar aparelhos | funciona | abre onde o e-mail foi lido |

Ambos são aceitos (OWASP Forgot Password; NIST §4.2.1.2). Link: não montar a URL a partir do
header `Host`. Validade máxima (NIST): **10 min** por SMS/voz, **24 h** por e-mail.

## 3. 🔴 Palpites acumulados entre códigos

Achado típico em auditoria: o contador de palpites **zera a cada código novo** → 5 códigos × 5
palpites = **25/h por conta**; ~600/dia ≈ 0,06%/dia; ~1,8% em 30 dias contra **uma** conta.
NIST §3.2.2 pede teto de falhas **consecutivas na conta** (≤ 100); *"Generating a new authentication
secret SHALL NOT reset the failed authentication count."* → contador **por conta e finalidade** que
sobrevive ao código novo; no teto, bloqueia a recuperação por um prazo e avisa a pessoa (cuidado com
o DoS do dono).

## 4. Qual canal (segurança > conveniência)

| Atacante controla | Reset por e-mail | Reset por WhatsApp/SMS |
|---|---|---|
| só o e-mail | troca a senha mas **para no 2º fator** do login | — |
| só o telefone (SIM swap, WhatsApp clonado) | — | troca a senha **e** recebe o código do login: **toma a conta** |

Se o telefone é o 2º fator do login, recuperar pelo telefone usa **o mesmo fator** duas vezes.
ASVS **6.4.3**: reset *"does not bypass any enabled multi-factor authentication mechanisms"*.
**Padrão recomendado: recuperação só por e-mail** (o WhatsApp como alternativa após 60 s não
fecha o buraco). Bônus: e-mail ~44–70× mais barato que WhatsApp por código. Quem perdeu o e-mail
vai ao SAC. Conta com e-mail **não verificado** não recupera por ele.

## 5. Mensagens e avisos

- Mensagem consistente para conta existente/inexistente (OWASP).
- Rate limit por conta + captcha (OWASP; ASVS 6.6.3).
- Recusa por limite: no "esqueci a senha" a tela não pode revelar nada — registrar só no log.
- Aviso de senha redefinida a **todos** os endereços de notificação (NIST §4.6), com instrução de "não fui eu".
- Remetente do código **separado** do de ofertas (Gmail recomenda um remetente por categoria).
