# Vulnerabilidades técnicas (a falha no código)

> **Revisado em:** 2026-10-07 · **Origem:** conteúdo compilado de fontes públicas (OWASP, ASVS, NIST, CWE, documentação oficial, avisos de CVE e artigos técnicos) — ver [referências](referencias-gerais.md). Se a data estiver antiga (> 6 meses) ou o tema envolver versão/preço/CVE, confirme na fonte oficial antes de aplicar.

> Catálogo genérico, "onde o código pode falhar". Numeração própria desta base (V01…V24),
> em que V18–V24 cobrem lacunas comuns frente ao ASVS. Para cada uma: o que é, defesa, teste e
> exemplo. Mapeamento ASVS em
> [`04-asvs.md`](../fundamentos/asvs.md). Golpes de negócio (o "modus operandi") em
> [`03-vetores-de-ataque.md`](../fundamentos/vetores-de-ataque.md).

## V01. Webhook forjado ou reenviado (replay)

- **O que é:** alguém faz POST no endpoint de webhook fingindo ser o gateway, ou reenvia um evento legítimo várias vezes.
- **Dano:** "confirma" pagamento que não existiu; emite crédito/voucher duplicado.
- **Defesa (3 camadas — a 2ª é obrigatória):**
  1. Validar a **assinatura** (HMAC) do webhook, quando o gateway documenta.
  2. **Nunca confiar no payload**: revalidar o status com um GET na API do gateway pelo ID do pedido antes de agir. Funciona mesmo sem assinatura.
  3. **Idempotência**: guardar o `event_id` processado e ignorar repetição (locking — ASVS V2.3.4).
- **Teste:** POST forjado com payload "pago" → nada é emitido (o GET desmente). Mesmo evento 3× → 1 efeito.
- *Exemplo:* gateway que não documentava publicamente o header de assinatura; a revalidação por GET virou a camada obrigatória.

## V02. Race condition / TOCTOU (uso ou pagamento em dobro)

- **O que é:** entre "verificar se pode" e "efetivar", requisições simultâneas passam pela verificação.
- **Dano:** voucher resgatado 2×; dois pedidos pagos com uma cobrança; saldo multiplicado por reembolso paralelo.
- **Defesa:** operação **atômica** — transação com `SELECT ... FOR UPDATE`, incremento atômico (`SET saldo = saldo - preco WHERE saldo >= preco`), lock no Redis, índice único. Check e uso no mesmo bloco (ASVS V15.4.2).
- **Teste:** 20 requisições simultâneas de resgate do mesmo item → só 1 sucesso.

## V03. Confiar no frontend (valor ou campo de compliance)

- **O que é:** o cliente altera dado na requisição (preço, quantidade, desconto, flag) e o servidor aceita.
- **Defesa:** o backend recalcula tudo a partir do banco e ignora valor do cliente; campo de compliance e identificador público (`slug`, `short_code`) são **derivados/gerados no servidor**; regras de tempo/liberação ("released") validadas no servidor.
- **Teste:** interceptar o checkout e alterar preço → pedido criado com preço correto ou recusado. Enviar o campo derivado no `PATCH` → ignorado/422.
- *Exemplos:* loja virtual (preço do procedimento); CMS com fotos de pacientes (`requires_consent` derivado de `is_sensitive`).

## V04. IDOR / BOLA (acessar recurso alheio ou de outra classe de sensibilidade)

- **O que é:** trocar o ID na URL/payload e acessar o que não deveria.
- **Defesa:** verificar **dono do recurso** em toda leitura/escrita; o ID do usuário vem **sempre da sessão/JWT**, nunca do corpo. Sem usuário final, a versão relevante é a **autorização por objeto**: um recurso mais sensível (ex.: mídia privada/termo assinado) exige permissão própria, não a genérica do módulo. IDs não sequenciais (UUID) reduzem enumeração em massa.
- **Teste:** logado como A, `GET /recurso/{id_do_B}` → 403/404. Com permissão genérica de mídia e sem a permissão de termos, pedir a mídia privada → 403.
- *Achado típico em auditoria:* `GET /api/admin/media/{id}/file` servia arquivo privado (termo com nome de paciente) só com `media:read`, contornando a permissão dedicada `consents`; e `id` era inteiro sequencial.

## V05. Exposição de dados sensíveis na resposta

- **O que é:** a API devolve mais campo do que a tela precisa (CPF, telefone, e-mail, hash de senha, nome de paciente, `consent_id`).
- **Defesa:** **schema de saída explícito** (`response_model`) em toda rota; projeção por público no serviço (schema público ≠ schema admin); segredo de configuração sai mascarado. Rota sem `response_model` só com justificativa escrita no docstring.
- **Teste:** inspecionar o JSON de cada endpoint público → nenhum campo sensível. Teste automatizado visto reprovando ao pôr um campo sensível no schema.

## V06. Mass assignment

- **O que é:** enviar campos extras num update e alterar o que não deveria (`{"role":"admin"}`, `{"saldo":999}`, `{"is_superuser":true}`).
- **Defesa:** whitelist de campos por endpoint; campo perigoso não existe no schema de entrada; atribuição campo a campo (nunca `**payload` sobre o model); `extra="forbid"` (campo a mais vira 422 em vez de ser descartado em silêncio — mantém o sinal de sondagem).
- **Teste:** enviar campo não permitido → 422 (ou ignorado, com o comportamento documentado).

## V07. Autenticação fraca / brute force

- **Defesa:** Argon2id + salt + pepper; rate limit por IP **e** por identidade; lockout por conta; captcha onde couber; mensagem e tempo iguais para conta inexistente; senha mínima longa; **MFA no admin**.
- **Teste:** N tentativas erradas → bloqueio/desafio (429/lockout). Conferir no banco que a senha não está em claro e o hash é `$argon2id$`.
- Detalhes em [autenticacao/senhas-hash-e-pepper](../autenticacao/senhas-hash-e-pepper.md).

## V08. Sessão insegura

- **Defesa:** token aleatório e longo (CSPRNG ≥ 128 bits); cookies `HttpOnly` + `Secure` + `SameSite` (prefixo `__Host-` quando possível); access curto; refresh opaco rotativo guardado como hash, com detecção de reuso; logout invalida de fato; JWT sem claim de privilégio. Nunca derivar token de credencial (ex.: SHA-256 da senha como token).
- **Gap comum:** JWT sem `jti`/denylist continua válido até expirar após o logout — aceitável só com TTL curto (ex.: 15 min) e documentado.
- **Teste:** `document.cookie` no console não mostra o cookie de sessão; token expirado → 401; após logout, o refresh antigo → 401.

## V09. SQL injection

- **Defesa:** ORM/prepared statements sempre, inclusive em upsert de integração; **nome de coluna não é parametrizável** → ordenação dinâmica por dicionário-allowlist; `order_dir` com `pattern="^(asc|desc)$"`. `ilike(f"%{q}%")` com valor como bind param é seguro (interpola o valor, não a query).
- **Teste:** `' OR 1=1--` em busca/login → sem erro de SQL e sem retorno indevido; `order_by=1;DROP` → cai no default. `grep` por `text(`/f-string em SQL.

## V10. XSS

- **Defesa:** escapar **no destino** (HTML, e-mail HTML, PDF, CSV, JSON-LD têm escapes diferentes); não sanitizar na entrada (corrompe `O'Brien`); não usar `dangerouslySetInnerHTML` com conteúdo de usuário/CMS; escapar `<`, `>`, `&` em JSON dentro de `<script>`; validar esquema de URL antes de virar `href`; SVG fora do upload; **CSP**.
- **Teste:** gravar `<script>alert(1)</script>` e `</script><script>…` nos campos editáveis → renderiza como texto; `javascript:alert(1)` em campo de URL → recusado.
- Detalhes em [headers](../headers/README.md).

## V11. CSRF

- **Defesa:** token anti-CSRF (double-submit com `hmac.compare_digest`) em todo método que muda estado, declarado no **router inteiro**; `SameSite=Lax/Strict`; funções sensíveis nunca via GET; ações públicas com efeito colateral conferem `Origin`/`Referer`.
- **Teste:** submeter formulário de outro domínio para a API → rejeitado; POST sem header CSRF → 403.

## V12. Upload de arquivo malicioso

- **Defesa:** tipo real por magic bytes (ignora extensão e `Content-Type`); whitelist JPEG/PNG/WebP; **SVG fora**; dimensão antes do decode (decompression bomb); nome aleatório (o enviado é descartado); limite de tamanho no app e na borda; fora do webroot ou com `autoindex off`; **metadado removido** (EXIF/GPS/miniatura).
- **Teste:** `.php`/`.html` renomeado para `.jpg` → recusado; SVG com `<script>` → recusado; `../../etc/passwd` como nome → arquivo gravado como `<uuid>.ext` dentro do diretório; foto com GPS → baixada sem GPS.
- Detalhes em [upload](../upload/README.md).

## V13. Falta de rate limit (abuso, card testing, raspagem)

- **Defesa:** rate limit por IP **e** identidade no login, checkout, cadastro, envio de OTP, rotas caras e rotas que servem acervo sensível; na borda e na aplicação; storage compartilhado entre workers (Redis) ou limite de borda como teto real.
- **Teste:** 100 requisições/min no checkout → 429; navegação normal → **zero** 429.
- Detalhes em [rate-limit](../rate-limit/README.md).

## V14. Segredos expostos

- **Defesa:** segredo fora do git (`.env`/secrets), fora do bundle do front (só `NEXT_PUBLIC_*` não sensível), fora do `docker inspect` (`secrets:`), app recusa placeholder, rotação, credencial de integração com privilégio mínimo e token de curta duração, segredos **distintos por ambiente**.
- **Teste:** `gitleaks detect` (histórico incluso); busca no bundle; `docker inspect` sem valor de segredo.
- Detalhes em [segredos](../segredos/README.md).

## V15. Dependências vulneráveis

- **Defesa:** `pip-audit`/`npm audit` no CI bloqueando crítico/alto; Dependabot; piso de versão explícito com motivo comentado onde houve CVE; prazo de remediação por severidade documentado; SBOM. Vulnerabilidade sem correção upstream: documentar por que não é explorável e monitorar.

## V16. Configuração incorreta (misconfiguration)

- **Defesa:** HTTPS + HSTS; debug off; `/docs` off; portas desnecessárias fechadas; banco não exposto; headers de segurança (+ CSP); sem directory listing nem TRACE; `.git`/`.env` não servidos; CORS sem `*`.
- **Teste:** varredura de portas + checagem de headers + `curl` em `/.git/config` e `/.env` → 403/404.

## V17. Falta de logs e auditoria

- **Defesa:** log de login (sucesso, falha, lockout), alteração de dado, ação sobre dado sensível (inclusive **leitura/download** e **delete**), eventos de pagamento, valor antes/depois em mudança de configuração; alertas. Ver [logs](../logs/README.md).
- **Teste:** executar a ação sensível → existe registro rastreável (quem, quando, onde, o quê).

## V18. SSRF (Server-Side Request Forgery) — ASVS V1.3.6

- **Quando se aplica:** o backend faz requisição de saída para URL que vem de fora (avatar de login social, importar imagem por URL, webhook configurável, callback).
- **Defesa:** função central de "saída segura": **HTTPS + allowlist de host + todo IP resolvido tem de ser global** (bloqueia `169.254.169.254`, redes privadas, loopback, **CGNAT `100.64.0.0/10`**, NAT64 `64:ff9b::/96`, multicast, reservados) + `follow_redirects=False` (um 302 de host permitido para IP interno escaparia).
- **Armadilha medida (Python 3.12):** `100.64.0.1` tem `is_private=False` e `is_global=False` — bloquear só `is_private` deixa o CGNAT passar; a regra correta é "só `is_global`" (e não multicast/reservado). DNS rebinding (resolução dupla) fica como risco aceito e documentado quando exigiria dominar o DNS do provedor.
- **Teste:** host da allowlist que resolve para `169.254.169.254`/`10.0.0.5`/`100.64.0.1` → recusado sem tocar a rede.
- **N/A quando:** não há chamada de saída originada de entrada (URLs fixas de config). Reentra no escopo ao surgir importação por URL, webhook configurável ou integração externa.

## V19. Portal do gateway comprometido (desvio do recebimento)

- **O que é:** o atacante entra no portal web do gateway/adquirente (força bruta, phishing, senha reaproveitada) e muda **para onde vai o dinheiro** (chave Pix, PSP recebedor, domicílio). Golpe BEC. Não passa pelo seu código.
- **Defesa:** ver [`11-gateway-de-pagamento.md`](../pagamentos/portal-do-gateway.md).

## V20. Login humano de sistema externo (CMS/ERP) sem MFA

- **O que é:** um sistema de terceiro que publica conteúdo/preço pela sua API de administração. Quem entra nele herda esse poder — allowlist de IP não protege, porque a requisição sai do servidor legítimo.
- **Defesa:** MFA obrigatório no login humano do sistema externo (PCI DSS 8.4.1), rate limit/lockout, log de quem publicou o quê. Item depende de quem opera o sistema externo — registrar o dono.

## V21. Campo de imagem/URL aceita qualquer host

- **O que é:** campo de arte/banner/avatar aceita qualquer URL HTTPS. Com a credencial do CMS, vira pichação da home com imagem do atacante; ou **tracker de IP** dos visitantes.
- **Defesa:** allowlist de host (o seu storage), no mesmo molde da saída segura; `data:` recusado; `remotePatterns` restritos no otimizador de imagem.
- **Teste:** `POST` com imagem de host fora da allowlist → 422.

## V22. Conta de teste ou seed chegando à produção

- **O que é:** conta de dev/QA/demonstração com senha conhecida, sem MFA, às vezes com privilégio, sobrevivendo no banco de produção.
- **Defesa:** seed de desenvolvimento nunca roda com `ENV=production`; checagem no go-live: nenhuma conta com e-mail de teste/domínio de exemplo.
- **Teste:** subir a produção do zero num ambiente descartável → `SELECT` em usuários/credenciais retorna vazio.

## V23. Classificação de dado e retenção — ASVS V14.1.1/V14.1.2/V14.2.7

- Sem tabela "campo → nível → controle mínimo" e sem expurgo programado, não se prova cobertura em auditoria LGPD. Ver [privacidade](../privacidade/README.md).

## V24. Vazamento por cache, `Referer` e storage do navegador — ASVS V3.4.5, V14.3.2, V14.3.3

- **Defesa:** `Referrer-Policy: strict-origin-when-cross-origin` (ou `no-referrer` em página com token); `Cache-Control: no-store` em toda resposta autenticada ou com PII (inclusive arquivo privado); nada sensível em `localStorage` (preferir `sessionStorage` ou nada); termo de busca sensível fora da URL (POST).
- *Padrão recomendado:* os headers saem da dependência de autenticação, então toda rota autenticada herda; `localStorage` auditado com zero ocorrências.

## Antes do go-live

- [ ] Todas as críticas implementadas **e** testadas (teste visto reprovando).
- [ ] Gaps do ASVS avaliados e decididos (entra/não entra).
- [ ] Varredura de dependências sem crítico/alto em aberto.
- [ ] Revisão ponta a ponta dos fluxos de dinheiro e de dado sensível.
- [ ] (recomendado) Pentest externo.
