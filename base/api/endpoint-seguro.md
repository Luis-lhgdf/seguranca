# Endpoint seguro: anatomia e bateria de testes

> **Revisado em:** 2026-10-07 · **Origem:** conteúdo compilado de fontes públicas (OWASP, ASVS, NIST, CWE, documentação oficial, avisos de CVE e artigos técnicos) — ver [referências](referencias.md). Se a data estiver antiga (> 6 meses) ou o tema envolver versão/preço/CVE, confirme na fonte oficial antes de aplicar.

> Segurança de endpoint não se resolve por lembrança: ou vira lista executada, ou escapa.
> *Exemplo típico (loja virtual):* cadastro e login nasceram com Argon2id, pepper, rate limit,
> anti-enumeração e schema explícito — e mesmo assim **três entradas passavam** (null byte,
> RTL override, homoglyph), achadas sondando os schemas no mesmo dia.

## 1. Anatomia (o método, independente de stack)

Caminho fixo: **router → dependências → schema de entrada → serviço → schema de saída.**
Nenhum endpoint monta query; nenhum serviço devolve objeto ORM para a camada HTTP.

| | Rota pública | Rota admin/autenticada |
|---|---|---|
| Autenticação | nenhuma | cookie de sessão/JWT |
| Autorização | o filtro é o `WHERE` do serviço (só publicado) | dono do recurso ou `require(módulo, ação)`/superuser |
| CSRF | GET não muda estado; POST público confere `Origin`/`Referer` | double-submit no **router inteiro** |
| Rate limit | borda + app nas rotas de escrita e nas que servem acervo sensível | borda + app no login/refresh |
| Saída | schema mínimo | schema do painel |
| Auditoria | — | antes do commit, nas ações sensíveis |

### Passo 1 — Dependências transversais no router, não na rota

CSRF e permissão declarados uma vez no `APIRouter`; guards como constantes nomeadas
(`_read`, `_create`, `_update`, `_delete`). Módulo inteiro de administração → guard de superuser
no router. Rota pública de escrita → origem própria + limite. ⚠️ `@limiter.limit` do slowapi
**exige** `request: Request` na assinatura — sem ele, estoura em runtime na primeira chamada.

### Passo 2 — Schema de entrada com teto em tudo

Todo `str` com `max_length`; toda `list` com `max_length`; todo id com `ge`; `Query` de domínio
fechado com `pattern` (ou `Literal`). Sem isso, um typo no filtro vira "sem filtro" em silêncio
(ex.: `sensitive=tru` trazendo conteúdo +18 junto). Campo **derivado nunca entra pelo schema** —
e o schema diz isso num comentário. `extra="forbid"`. O 422 sai traduzido por handler global, sem
vazar interno.

### Passo 3 — Regra no serviço; o endpoint não monta query

Ordenação vinda do cliente por **dicionário-allowlist** (o `dict` é o validador: fora dele, cai no
default). Referência a id de outra tabela checada **antes** do insert (404 claro em vez de 500 de FK).

### Passo 4 — Bloqueio de negócio como exceção tipada, com rollback

O serviço levanta exceção própria (`PublishBlocked`, `UploadError`); o endpoint faz
`rollback()` e converte em 4xx. Ler `max_bytes + 1` no upload para detectar excesso em vez de truncar.

### Passo 5 — Auditoria antes do commit

`audit.record()` adiciona na mesma sessão; persiste junto com a ação. Ação falhou → log some junto.
O `action` carrega o desfecho (`result.create.published`, `consent.revoke(unpublished=3)`).

### Passo 6 — Schema de saída sempre, montado no serviço

Duas camadas: o serviço projeta só os campos daquele público; o `response_model` filtra de novo.
Mesmo recurso, dois contratos (`*PublicRead` × `*AdminRead`). Recurso sensível em endpoint
separado do metadado (preview social/OG nunca carrega a mídia sensível). Segredo de config mascarado.

### Passo 7 — Erro que não ensina nada

Mesma resposta para "não existe" e "não é seu"; mesmo custo de CPU onde o tempo vira oráculo;
erro sem stack, sem SQL, sem nome de coluna. `/docs` e `/openapi.json` desligados em produção.

### Passo 8 — Saber onde está o limite real

Limite no app em memória é **por processo** (2 workers = o dobro); o teto real é o da borda
(Nginx) ou um storage compartilhado (Redis). Documentar.

## 2. A bateria (campo a campo, em toda rota que aceita entrada)

### 2.1 Bytes e comprimento

| Payload | Por quê |
|---|---|
| `\x00` (null byte) | Postgres recusa `NUL` em `TEXT`/`VARCHAR` → **500 provocável por qualquer um** em vez de 422 (comportamento medido). MySQL se comporta diferente — **testar**, não presumir |
| `"A" * 10_000` | todo `str` precisa de `max_length` |
| `"A" * 1_000_000` | trabalho caro (Argon2, regex, full-text, Pillow) sobre lixo |
| vazio e só espaços | `strip` transforma `"   "` em `""` — `min_length` pega? |
| corpo sem `Content-Length` (`Transfer-Encoding: chunked`) | middleware que só lê o header deixa passar; quem segura é a borda |

### 2.2 Unicode

| Payload | Por quê |
|---|---|
| `U+202E` RTL override | inverte nome na tela, no e-mail, no voucher |
| `U+200B` zero-width | dois cadastros "iguais" que o `UNIQUE` deixa passar |
| homoglyph (`а` cirílico, `ı` turco) | parece o e-mail do admin e não é |
| emoji / plano astral | decidir **e escrever** se aceita |
| `\r\n` em campo que vira cabeçalho | header injection em e-mail (assunto, `From`) |

### 2.3 Injeção — pelo destino final, não pelo banco

| Payload | Onde machuca |
|---|---|
| `<script>`, `<img onerror>` | e-mail HTML, PDF, painel do SAC, JSON-LD |
| `=1+1+cmd\|' /C calc'!A0` | CSV exportado (fórmula executa no Excel) — ASVS V1.2.10 |
| `{{7*7}}`, `${...}` | template de e-mail/mensagem; template string do front |
| `../../etc/passwd` | campo que vira nome de arquivo |
| `http://169.254.169.254/` | SSRF em qualquer URL vinda do cliente |
| `javascript:alert(1)`, `data:` | campo de URL que vira `href` |

### 2.4 Forma

- tipo trocado: número onde espera string, lista onde espera objeto, `null` explícito;
- **número fracionado e `NaN` onde se espera inteiro** (`1.5` em estrelas/quantidade/coordenada — derruba runtime ou fura lógica);
- campo a mais (→ `extra="forbid"`); obrigatório ausente; JSON malformado; corpo vazio; `Content-Type` errado.

### 2.5 Abuso

- rate limit por IP **e** por identidade (só IP cai com proxy; só identidade cai com conta descartável);
- captcha em rota pública de escrita que um humano envia ([captcha/captcha-turnstile](../captcha/captcha-turnstile.md));
- **custo por requisição** (Argon2 ~50 ms, e-mail/SMS/WhatsApp custam dinheiro, full-text é I/O) — rota cara sem limite é DoS barato;
- idempotência onde repetir causa dano.

### 2.6 Saída

- schema explícito; "não existe" = "não é seu"; mesmo custo de CPU; erro sem stack;
- 🔴 nenhum vínculo **pessoa ↔ dado sensível** (ex.: pessoa ↔ procedimento) em URL, log ou mensagem.

### 2.7 O que fazer com cada resultado

| Categoria | Tratamento |
|---|---|
| Controle (`\x00`, `U+202E`, `U+200B`) | **recusar na entrada** (422, mensagem clara) |
| Comprimento | `max_length` em **todo** campo, inclusive os com validador próprio |
| Homoglyph | recusar, ou normalizar e comparar — decidir por campo e registrar |
| Emoji | decisão explícita |
| `<script>` e afins | **guardar como veio, escapar na saída** — cada destino tem o seu escape |

⚠️ Sanitizar na entrada é a solução errada para `<script>`: corrompe nome legítimo
(`O'Brien`, `Müller`) e dá falsa segurança. Filtro por lista de palavras (`<script>` minúsculo)
é contornado com maiúscula ou outra tag.

## 3. Checklist de revisão de um endpoint novo (perguntas ao ler o diff)

**Router e dependências**
- CSRF no router (admin, sempre — mesmo que hoje só tenha GET)?
- `require(módulo, ação)` com a **ação certa** (não reaproveitar `_read` num POST)?
- Módulo certo (dado sensível tem permissão própria)?
- Rota pública de escrita com conferência de origem **e** rate limit?
- Rota entrou no agregador de rotas (onde se vê a superfície inteira)?

**Entrada**
- `max_length`/`ge`/`pattern` em tudo? Campo derivado aceito do cliente? Ordenação por allowlist?
  Referência a outra tabela checada antes? URL com esquema validado?

**Saída**
- `response_model` explícito do público certo? Algum campo identifica pessoa (nome, id de termo,
  nome de arquivo original, EXIF)? Mídia sensível em endpoint separado? Segredo mascarado?

**Efeito e rastro**
- Ação irreversível ou sobre PII audita **antes** do commit? `action` diz o desfecho?
  Exceção tipada com rollback? Mensagens iguais onde a diferença viraria oráculo?

**Teste**
- Existe teste do 401/403 além do 200? A bateria (§2) foi rodada? Algum teste foi visto reprovando?

## 4. Registro

O resultado da bateria vai para o card/issue da feature, com data e o que foi testado
(PR fecha e some; card fica) — ou para o relatório de auditoria desta base.
