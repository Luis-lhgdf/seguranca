# Portal do gateway: o golpe da conta recebedora (BEC)

> **Revisado em:** 2026-10-07 · **Origem:** conteúdo compilado de fontes públicas (OWASP, ASVS, NIST, CWE, documentação oficial, avisos de CVE e artigos técnicos) — ver [referências](referencias.md). Se a data estiver antiga (> 6 meses) ou o tema envolver versão/CVE, confirme na fonte oficial antes de aplicar.

## 1. O golpe

- **BEC:** o atacante entra numa conta legítima e **muda o destino do dinheiro**. FBI/IC3 PSA240911: 305.033 incidentes, US$ 55,5 bi (out/2013–dez/2023).
- Entrada: força bruta, *password spraying*, phishing, senha reaproveitada (CISA AA24-290A); *push bombing* de MFA.
- Não passa pelo seu código — o portal é do gateway.

## 2. Onde o dinheiro pode ser desviado

- **Pix:** chave Pix e credencial do PSP recebedor costumam ser cadastradas **e editáveis** no portal do lojista → plausível desviar pelo portal; o 2FA é a única barreira documentada.
- **Cartão:** no Brasil, a liquidação segue o domicílio informado pela **registradora de recebíveis** (Res. BCB 264/2022; Res. CMN 4.734/2019) — não um campo do portal; confirmar com o gateway se algum campo editável (código de estabelecimento) redireciona a venda.
- Recuperação de senha por e-mail faz do **e-mail do usuário** um segundo alvo.
- Situação comum em portais de lojista: 2FA (Google Authenticator) **opcional** e ligado usuário por usuário; bloqueio por tentativas e log de auditoria não documentados.

## 3. Checklist de configuração (antes do go-live)

- [ ] 2FA ligado em **todos** os usuários, não só no admin (PCI DSS 8.4.1); preferir FIDO/WebAuthn se disponível.
- [ ] **Um login por pessoa** — nenhuma conta compartilhada.
- [ ] Mínimo privilégio: perfis de administração com o menor número de pessoas; cancelamento separado de relatórios.
- [ ] Senha longa e única; **e-mail de recuperação também com MFA**.
- [ ] Revisão de acessos periódica; quem saiu perde o acesso no dia.
- [ ] Mudança de chave Pix, PSP, código de estabelecimento ou domicílio: **confirmação fora de banda** (telefone já conhecido + segunda pessoa) — recomendação do IC3.
- [ ] **Conciliação diária**: liquidado × vendido, e o domicílio na agenda de recebíveis.
- [ ] Perguntar ao gateway: bloqueio por tentativas, log de auditoria, aviso de alteração de dado bancário.

## 4. CMS/sistemas que publicam preço

O mesmo raciocínio vale para qualquer sistema externo que altera preço ou conteúdo pela sua API
de administração: MFA no login humano dele, log de quem publicou o quê.
