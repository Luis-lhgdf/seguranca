# XSS: escape por destino

> **Revisado em:** 2026-10-07 · **Origem:** conteúdo compilado de fontes públicas (OWASP, ASVS, NIST, CWE, documentação oficial, avisos de CVE e artigos técnicos) — ver [referências](referencias.md). Se a data estiver antiga (> 6 meses) ou o tema envolver versão/CVE, confirme na fonte oficial antes de aplicar.

## 1. Regra

**Guardar como veio, escapar na saída** — cada destino tem o seu escape. Sanitizar na entrada
corrompe dado legítimo e dá falsa segurança; filtro por lista de palavras é contornado.

| Destino | Escape/defesa |
|---|---|
| HTML via React/Vue | escape automático; **proibido** `dangerouslySetInnerHTML`/`v-html` com conteúdo de usuário/CMS |
| JSON dentro de `<script>` (JSON-LD, estado inicial) | `JSON.stringify` **não** escapa `<`, `>`, `/` → substituir `<` `>` `&` por `<` `>` `&` (o JSON continua válido) |
| Atributo `href`/`src` | validar esquema (`https:`, `http:`, `mailto:`, `tel:`) — `javascript:` e `data:` executam; no **backend** (`HttpUrl` ou validador), que vale para qualquer cliente |
| E-mail HTML, PDF | template com autoescape |
| CSV/planilha | prefixar `'` em valor que começa com `=`, `+`, `-`, `@` (Formula Injection, ASVS V1.2.10) |
| Template de mensagem/e-mail | não avaliar entrada como template (`{{7*7}}`, `${}`) |
| Cabeçalho de e-mail | recusar `\r\n` |

## 2. Caso típico — XSS armazenado no JSON-LD

- Componente de SEO: `dangerouslySetInnerHTML={{ __html: JSON.stringify(business) }}` com campos editáveis no CMS (nome, endereço, Instagram, WhatsApp) renderizado em **todas** as páginas.
- Valor `Nome</script><script>…</script>` fecha a tag e executa contra **visitantes**.
- Agravantes: o valor da configuração era `Any` sem limite; o site público e o `/admin` na **mesma origem** com cookie CSRF legível → script plantado por um operador com permissão só de configuração roda quando o superuser visita a home e faz mutações como superuser.
- Correção na origem: escape de `<`, `>`, `&`; tipar e limitar o valor por chave; CSP como rede. Verificação em produção: `curl -s $SITE/ | grep -o '<script type="application/ld+json">[^<]*<'` sem `<` cru no conteúdo.

## 3. Outros sinks a procurar

```bash
grep -rnE "dangerouslySetInnerHTML|v-html|innerHTML\s*=|insertAdjacentHTML|document\.write|eval\(|new Function\(" $REPO/<front>
grep -rnE "href=\{[^}]*(url|link|href)" $REPO/<front>
```

Para cada ocorrência: a origem do dado é controlável por usuário/CMS? há escape/validação?

## 4. Teste

Gravar (em teste) `<script>alert(1)</script>`, `"><img src=x onerror=alert(1)>`, `</script><script>alert(1)</script>`
e `javascript:alert(1)` em cada campo editável → tudo renderiza como texto ou é recusado.
