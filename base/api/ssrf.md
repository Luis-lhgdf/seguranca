# SSRF — requisição de saída com URL vinda de fora

> **Revisado em:** 2026-10-07 · **Origem:** conteúdo compilado de fontes públicas (OWASP, ASVS, NIST, CWE, documentação oficial, avisos de CVE e artigos técnicos) — ver [referências](referencias.md). Se a data estiver antiga (> 6 meses) ou o tema envolver versão/CVE, confirme na fonte oficial antes de aplicar.

ASVS **V1.3.6** (L2): validar dado não confiável contra allowlist de protocolo/domínio/porta antes
de usá-lo para chamar outro serviço.

## 1. Quando se aplica

Inventariar **toda** chamada HTTP de saída do backend (`requests`, `httpx`, `aiohttp`, `urllib`,
`fetch`, `axios`) e classificar:

| Tipo de saída | SSRF? |
|---|---|
| URL fixa/de configuração (captcha, gateway, WhatsApp, OAuth, revalidação) | não |
| URL vinda de usuário, de provedor externo ou do admin (avatar do login social, importar imagem por URL, webhook configurável, callback) | **sim** |
| Otimizador de imagem do front (`remotePatterns`) com host remoto aberto | sim (no servidor do front) |

*Exemplo (loja virtual):* 5 saídas; só 1 com URL de fora — a foto de perfil devolvida pelo
Google/Facebook no login social. *Exemplo (site institucional estático com painel):* nenhuma saída em produção (cliente HTTP só
em dependência de dev; `remotePatterns: []`) → **N/A**, com gatilho de reentrada.

## 2. Defesa — função central de "saída segura"

1. **HTTPS** obrigatório.
2. **Allowlist de host**.
3. **Todo IP resolvido** tem de ser **global**: bloqueia `169.254.169.254` (metadados de nuvem), `10/8`, `172.16/12`, `192.168/16`, loopback, link-local, **CGNAT `100.64.0.0/10`**, NAT64 `64:ff9b::/96`, multicast, reservados, e as formas IPv4-mapeadas (`::ffff:100.64.0.1`).
4. **`follow_redirects=False`** em quem baixa (um 302 de host permitido para IP interno escaparia).
5. Timeout curto, limite de tamanho da resposta.

🔴 **Armadilhas medidas (Python 3.12):**
- `ipaddress.ip_address("100.64.0.1")`: `is_private=False` **e** `is_global=False` → bloquear só `is_private` deixa o CGNAT passar. Regra: **"só `is_global`"** e, além disso, recusar multicast e reservado.
- NAT64 e multicast dão `is_global=True` → precisam de recusa explícita.
- **DNS rebinding** (o host é resolvido duas vezes: na validação e na conexão): mitigar conectando no IP validado; ou aceitar e documentar quando exigiria dominar o DNS do provedor (risco aceito documentado).

## 3. Teste

- Host da allowlist que resolve para `169.254.169.254`, `10.0.0.5`, `100.64.0.1`, `100.127.255.254`, `::ffff:100.64.0.1` → recusado **sem tocar a rede**.
- Redirect 302 para IP interno → não seguido.
- Teste visto reprovando ao remover o bloqueio de IP.

## 4. Variante no front: tracker de IP e host de imagem livre

Campo que aceita URL de imagem externa (avatar, banner) faz o **navegador do visitante** buscar no
servidor do atacante (IP, horário) — ou permite pichar a home. Defesa: allowlist de host da imagem
(o seu storage); `data:` recusado; otimizador sem `remotePatterns` abertos.
