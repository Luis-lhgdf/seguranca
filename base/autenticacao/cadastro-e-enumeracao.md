# Cadastro: contas falsas, verificação de e-mail e enumeração

> **Revisado em:** 2026-10-07 · **Origem:** conteúdo compilado de fontes públicas (OWASP, ASVS, NIST, CWE, documentação oficial, avisos de CVE e artigos técnicos) — ver [referências](referencias.md). Se a data estiver antiga (> 6 meses) ou o tema envolver versão/preço/CVE, confirme na fonte oficial antes de aplicar.

Aplica-se quando há **cadastro self-service** de usuário final.

## 1. Cadastro em massa (OWASP OAT-019 Account Creation)

Primeiro, qual é o dano **no seu produto** (não copiar receita de SaaS):

| Dano | Peso típico (loja virtual de serviços de saúde) |
|---|---|
| recurso gratuito entupido (agenda de avaliação grátis) | alto |
| OTP queimado (cada envio custa dinheiro) | alto |
| cupom/promoção de 1º acesso | depende |
| base poluída, métrica distorcida | baixo |

O que o OWASP recomenda de fato:
- 🔴 *"Verify email **before** the account is usable; do not just send a confirmation, gate features behind it."* — o valor está em **barrar função** (agendar, usar cupom, comprar) enquanto não verificado. Coluna `email_verificado` que não barra nada é decoração.
- Velocidade de cadastro por **IP, ASN e impressão de dispositivo** (exemplo do cheat sheet: 3/h).
- Telefone: checar tipo de linha (VoIP é barato).
- Captcha é *last-resort step-up*, não o primeiro controle.

⚠️ O que o OWASP **não** recomenda: normalizar Gmail (tirar pontos/`+sufixo`) — *"Avoid
provider-specific transformations"*, *"Preserve the original email"*; bloquear lista de
descartáveis às cegas — *"prefer risk-based controls"*. Reabrir só com problema **medido**.
CPF com dígito válido não prova existência (é gerável).

## 2. E-mail de outra pessoa prendendo o endereço (sequestro)

Cenário reproduzível: atacante cadastra com `vitima@...` e o **próprio** celular → a dona
recebe 409 "já existe conta" (enumeração) e, se o "esqueci a senha" cair para outro canal, o
código vai para o atacante. Agravante: e-mail que não se troca prende o endereço para sempre.

Opções avaliadas:

| Opção | Fecha? | Contra |
|---|---|---|
| a. Dois códigos no cadastro (e-mail + celular) | sim | fricção; põe o provedor de e-mail (SPF/DKIM/sandbox) no caminho do cadastro |
| b. Não verificado **não reserva** o endereço (modelo Firebase: *"the trusted provider overwrites the untrusted"*) | sim | índice único parcial; a conta que perde fica sem login |
| c. Só celular, e-mail depois | não sozinha | — |
| d. Só e-mail no cadastro | sim | perde o celular como 2º fator |
| **e. "Não fui eu" no e-mail de boas-vindas** | sim, se a dona viu | link com token: tela + POST (scanner abre GET), uso único, hash, ≤ 24 h, só conta não verificada |
| **g. Cadastro com e-mail ocupado responde sempre igual e avisa o dono por e-mail** | sim, junto com e | — |

Recomendação técnica: **e + g** (1 código no cadastro, e-mail resolvido na caixa de
entrada, sem depender do provedor de e-mail para cadastrar). CPF duplicado também enumera e prende
o dono — alternativa usada na prática: o SAC resolve com documento.

## 3. Enumeração

- ASVS **6.3.8** (L3): não deduzir usuário válido — **cadastro e "esqueci a senha" também**.
- OWASP Email Validation: *"Attackers should not be able to determine whether an email is registered."*
- Resposta genérica no cadastro: *"Enviamos as instruções para o seu e-mail"*; o e-mail diz "você já tem conta, esqueceu a senha?" (verificada) ou "se não é sua, libere" (não verificada).
- Onde não dá para ter mensagem genérica, captcha + rate limit (OWASP Authentication CS).
- "Este celular já tem conta" também enumera — em serviço de saúde/estética, revelar que alguém é cliente é perto de dado sensível.

## 4. Normas

- NIST 800-63A-4 §3.8: código ≥ 6 dígitos; validade 10 min (telefone), 24 h (e-mail).
- NIST 800-63B-4 §4.2.1.2: endereço de **recuperação** só vale depois de verificado.
- ASVS 6.6.1: OTP por telefone só para número **já validado**.
- Nenhum requisito ASVS exige verificar e-mail **antes** de a conta existir — exige antes de **servir à recuperação**.

## 5. Usabilidade (o contrapeso)

Baymard: 18% abandonam por exigência de conta; 17% por checkout longo. NN/g (2017): evitar
confirmar cadastro por link de e-mail; se precisar, código por SMS. Pedir verificação no
checkout põe a fricção na pior hora.

## 6. Contas de teste

Seed de dev nunca roda com `ENV=production`; no go-live, nenhuma conta com e-mail de teste ou
domínio de exemplo (ver V22 em [fundamentos/vulnerabilidades](../fundamentos/vulnerabilidades.md)).
