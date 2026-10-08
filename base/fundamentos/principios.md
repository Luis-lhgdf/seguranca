# Princípios e boas práticas

> **Revisado em:** 2026-10-07 · **Origem:** conteúdo compilado de fontes públicas (OWASP, ASVS, NIST, CWE, documentação oficial, avisos de CVE e artigos técnicos) — ver [referências](referencias-gerais.md). Se a data estiver antiga (> 6 meses) ou o tema envolver versão/preço/CVE, confirme na fonte oficial antes de aplicar.

> Regras permanentes, válidas para todo código novo em qualquer projeto. Diferente de
> [`02-vulnerabilidades.md`](../fundamentos/vulnerabilidades.md) (ataque por ataque), aqui ficam os
> princípios.

## 1. Princípios inegociáveis

1. **Nunca confiar no cliente.** Toda validação, todo cálculo de valor e todo campo com efeito
   de compliance acontece no backend. Campo **derivado** (preço total, `requires_consent`,
   `slug`, contador, status) é calculado no servidor e nunca aceito do corpo da requisição.
   *Exemplo:* num CMS com fotos de pacientes, `requires_consent` (decide se publicar foto de paciente exige termo)
   é derivado de `is_sensitive` no serviço; se viesse do cliente, um `PATCH` publicaria foto sem termo.
2. **Menor privilégio.** Cada credencial acessa só o que precisa: usuário do banco da aplicação
   sem DDL, credencial de integração que escreve só o que deve (*exemplo:* numa loja virtual, a API
   de administração usada pelo CMS escreve só catálogo, não toca pedido, voucher nem cliente),
   contas de serviço sem sudo, permissão por módulo/ação no painel.
3. **Defesa em camadas.** Se uma proteção falhar, outra segura: validação + autorização + rate
   limit (borda **e** aplicação) + lockout + log + fail2ban. Limite de corpo no app **e** no Nginx.
4. **Falhar fechado.** Na dúvida, negar. Erro de configuração não pode liberar operação:
   a aplicação **não sobe** com segredo placeholder/curto, com `CORS=*`, com chave de captcha de
   teste em produção; bootstrap do primeiro admin exige token em produção e se desliga depois.
   (Exceção consciente e documentada: fail-open do captcha **no login**, ver [`07-captcha.md`](../captcha/captcha-turnstile.md).)
5. **Segurança não é fase.** O controle entra no mesmo commit da feature (autenticação, upload,
   pagamento, dado sensível), não "numa passada de segurança depois".
6. **Testar, não presumir.** *"Segurança não é o que você configura, é o que você testa"*. Teste
   que nunca foi visto **reprovando** não prova nada: desligue o controle, veja o teste falhar,
   religue. Documento é hipótese; só vale o que foi verificado no código ou no servidor.

## 2. Autenticação e acesso

- Hash de senha **Argon2id** com salt por hash + pepper fora do banco ([autenticacao/senhas-hash-e-pepper](../autenticacao/senhas-hash-e-pepper.md)).
- **MFA obrigatório** em toda conta administrativa (quem publica, edita preço, vê dado sensível);
  hash forte não substitui segundo fator (PCI DSS 8.4.1).
- Sessões curtas; logout invalida o token **no servidor**.
- Separar claramente superfície **pública** de **admin** (rotas, routers, layout do front).
- Toda rota autenticada verifica o **dono do recurso** (ou, sem usuário final, permissão por
  módulo+ação **relida do banco a cada requisição** — o token não carrega privilégio).

## 3. Dados

- **Dinheiro nunca em float**: `NUMERIC` no banco, `Decimal` no código. `float()` só para exibição.
- **Schemas de saída explícitos**: o que vai ao navegador é lista fechada de campos, nunca o model.
- **Minimização** (LGPD): não guardar nem servir dado sensível que não se usa; tirar metadado de imagem.
- **Backup automático, cifrado, fora do host e com teste de restauração** ([`16-infra-vps.md`](../copias-de-seguranca/README.md)).

## 4. Pagamento (quando houver)

- Deixar o **gateway processar o cartão** (checkout hospedado/iframe/tokenização) — reduz escopo PCI.
- **Idempotência** em criação de pedido, pagamento e emissão de crédito/voucher.
- Emissão/uso de recurso consumível sempre em **transação atômica**.
- Valor cobrado **sempre recalculado** no servidor.
- Estados do pedido/voucher bem definidos e auditáveis. Ver [pagamentos](../pagamentos/README.md).

## 5. Código e dependências

- Validação de entrada por **schema** (Pydantic, Zod, Joi) em **whitelist**, com tipagem estrita
  (rejeitar `1.5` onde se espera inteiro, `NaN`) e `max_length` em tudo.
- **ORM/prepared statements** em toda query; ordenação dinâmica por dicionário-allowlist.
- Sem segredo no código nem no bundle do front.
- `pip-audit`/`npm audit`, SAST e gitleaks **no CI, bloqueando** o merge/deploy.
- Code review obrigatório no que toca autenticação, upload, pagamento e dado sensível.
- Lockfile commitado e instalação determinística (`npm ci`, `uv sync --frozen`/`pip install --require-hashes`).

## 6. Infraestrutura

- HTTPS obrigatório + HSTS + cabeçalhos de segurança + **CSP no HTML** ([headers](../headers/README.md)).
- Banco, Redis e backend **não expostos** à internet (loopback ou rede interna do Docker).
- Integração de escrita vinda de fora: autenticação forte, allowlist de origem, privilégio mínimo, log.
- Debug desligado em produção; `/docs`/`/openapi.json` desligados; erro sem stack trace.
- Rate limit **na borda e na aplicação**.
- VPS endurecida ([`16-infra-vps.md`](../infra-vps/README.md)).

## 7. Operação

- Log de auditoria das ações sensíveis (login, falha, dado sensível, pagamento, permissões).
- **Alerta ativo** — não adianta logar e ninguém ver (Sentry, uptime externo, canal de notificação).
- **Plano de resposta a incidente** com o prazo de comunicação à ANPD/titulares (LGPD).
- Pessoas treinadas contra **phishing/BEC**; MFA nas contas corporativas satélites (e-mail,
  registrador de domínio, hospedagem, GitHub, redes sociais, portal do gateway).
- Operador único: senha exclusiva, desconfiar de link pedindo relogin, **nunca colar `.env`,
  token de setup ou chave em chat/IA**.
