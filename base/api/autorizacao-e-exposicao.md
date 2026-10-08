# Autorização, exposição de dados e superfície da API

> **Revisado em:** 2026-10-07 · **Origem:** conteúdo compilado de fontes públicas (OWASP, ASVS, NIST, CWE, documentação oficial, avisos de CVE e artigos técnicos) — ver [referências](referencias.md). Se a data estiver antiga (> 6 meses) ou o tema envolver versão/CVE, confirme na fonte oficial antes de aplicar.

## 1. Autorização (IDOR/BOLA, BFLA)

- **Com usuário final:** toda leitura/escrita verifica o **dono do recurso**; o id do usuário vem da sessão, nunca do corpo. "Não existe" e "não é seu" respondem igual (404).
- **Sem usuário final (painel):** permissão por **módulo + ação**, relida do banco a cada request; gestão de usuários só superuser (guard no router inteiro).
- **Autorização por objeto:** recurso mais sensível dentro de um módulo exige permissão própria. *Achado típico em auditoria:* num painel de clínica, o termo de consentimento (PII) tinha permissão dedicada `consents`, mas era servido como mídia privada sob `media:read` — quem só publica na galeria lia os termos. Correção: decidir o guard **depois** de carregar o objeto (`is_private` → exige `consents:read` ou superuser) e auditar também a rota de exibição, não só a de download.
- IDs sequenciais facilitam varredura; preferir UUID para recursos expostos.
- Rota "só autenticado" sem `require(...)` destoa do resto — documentar ou corrigir.
- Middleware do front (Next.js) **não é** autenticação; a API autoriza em toda requisição (CVE-2025-29927 afetou Next ≤ 15.2.2).

## 2. Exposição de dados na resposta

- `response_model` explícito em **toda** rota; schema público ≠ schema admin.
- Projeção no serviço (`to_public_read`) **e** filtro na borda HTTP.
- Nunca devolver o model ORM direto (campo novo no model vaza sozinho).
- Rota que devolve mapa dinâmico (ex.: `GET /settings` público) move a allowlist para o banco (`is_public`) — conferir as linhas marcadas públicas e restringir quem altera a flag.
- Segredo de configuração sai **mascarado** por padrão.
- Nada que ligue pessoa a dado sensível (nome ↔ procedimento, foto ↔ termo) em rota pública, URL, log ou mensagem de erro.

## 3. Mass assignment

- Schema `Update` fechado; `model_dump(exclude_unset=True)` só de schema declarado; atribuição campo a campo onde há privilégio.
- **`extra="forbid"`** (Pydantic v2 default é `ignore`: campo desconhecido é descartado em silêncio — apaga o sinal de sondagem). Duas abordagens aparecem na prática: `forbid` (recusa com 422 e deixa a sondagem visível — recomendado) e `ignore` (aceitável quando não há caminho de escalada, mas perde o sinal; recomendado ligar `forbid`).
- Campos derivados (`requires_consent`, `slug`, `short_code`, contadores, preço) **fora** do schema de entrada, com comentário dizendo por quê.

## 4. Superfície e configuração da API

- `/docs`, `/redoc`, `/openapi.json` desligados em produção.
- CORS com origens explícitas; `*` recusado no boot (cookie + curinga = sessão de qualquer um); métodos e headers restritos.
- Limite de corpo no middleware **e** na borda — middleware que só lê `Content-Length` deixa `Transfer-Encoding: chunked` passar.
- Erros sem stack/SQL; handler global de 422 sem vazar interno; 401/403 genéricos.
- Agregador único de rotas (`router.py`) — é onde se vê a superfície inteira; routers sem `prefix` com caminhos absolutos são onde rota nova nasce fora do router protegido.

## 5. Integrações e comunicação entre serviços (ASVS V13.1.1, V13.2.1, V13.2.2)

- Documentar **toda** integração: destino, credencial, privilégio, quem opera.
- Integração que **escreve** no seu sistema (ex.: CMS/ERP publicando catálogo pela "API de administração"): autenticação forte, allowlist de origem, privilégio mínimo (só o que precisa), token de curta duração em vez de credencial estática, log de auditoria; MFA no login humano do sistema externo (a allowlist de IP não protege contra quem entra no sistema legítimo).
- Rotas de integração **máquina a máquina** podem ficar fora do rate limit de usuário, mas isso deve estar coberto por teste/documentação.
- Limite documentado de conexões concorrentes por serviço externo (ASVS V13.1.2, L3).
- Sistema monolítico de host único (Next SSR → API → banco em loopback): basta documentar as ligações e o privilégio do usuário do banco.
- Aprovação dupla (four-eyes) para operação de alto valor (V2.3.5): pode morar no sistema consumidor (SAC/financeiro); do lado da API ficam as regras do dado (estorno ≤ valor pago, idempotência, campo `usuario` para histórico).
