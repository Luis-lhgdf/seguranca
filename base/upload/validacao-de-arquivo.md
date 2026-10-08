# Upload: validação do arquivo

> **Revisado em:** 2026-10-07 · **Origem:** conteúdo compilado de fontes públicas (OWASP, ASVS, NIST, CWE, documentação oficial, avisos de CVE e artigos técnicos) — ver [referências](referencias.md). Se a data estiver antiga (> 6 meses) ou o tema envolver versão/CVE, confirme na fonte oficial antes de aplicar.

O upload costuma ser o **único ponto onde bytes de terceiro entram no servidor**.

## 1. As defesas

| Defesa | Como |
|---|---|
| Tipo real | assinatura nos primeiros bytes (magic bytes): JPEG `FF D8 FF`, PNG `89 50 4E 47`, WebP `RIFF....WEBP`. Nome e `Content-Type` declarados **ignorados** |
| Whitelist | JPEG, PNG, WebP. **SVG fora** — é o único formato de imagem que executa script. GIF/HTML/PDF → 415/422 |
| Bomba de descompressão | dimensão lida do cabeçalho e comparada a um teto (ex.: 6000 px) **antes** de decodificar; `Image.MAX_IMAGE_PIXELS` fixado. PNG de 303 KB pode virar 286 MB de bitmap e 5,3 s de CPU (medido) |
| Nome aleatório | `uuid4().hex` + extensão do formato **reconhecido**; o nome enviado é **descartado**, não "higienizado" (`../../etc/passwd` vira `<uuid>.png` dentro do diretório) |
| Path traversal | destino validado contra o root com `os.path.commonpath` |
| Tamanho | leitura em pedaços, corta ao passar do teto e apaga o parcial; ler `max+1` bytes para detectar excesso; teto no app (ex.: 5 MB) **e** na borda (`client_max_body_size`) — 413 na borda |
| Fora do webroot / sem listagem | servido pelo Nginx em `/midia/` ou `/uploads/` com `autoindex off` e `X-Content-Type-Options: nosniff` |
| Arquivo "de mentira" | assinatura certa sem imagem (`FF D8 FF E0` + zeros) deve ser recusado — o parser tem de achar a estrutura (ex.: marcador `SOS` no JPEG) |
| Autorização | rota de upload autenticada e com permissão; sem token → 401 |

## 2. Testes que provam

- `.php` e `.html` renomeados para `.jpg`/`.png` → recusados.
- SVG com `<script>` → recusado.
- GIF → recusado (se fora da whitelist).
- `../../etc/passwd` como nome → gravado como `<uuid>.ext` no diretório certo.
- Arquivo acima do teto → 422 no app e 413 na borda.
- Sem sessão → 401.
- Testes vistos reprovando ao desligar cada defesa (ex.: uma suíte de 16 casos).

## 3. Serviço de arquivo e XSS

- Mesmo domínio dos cookies = arquivo hostil executa no contexto do site → SVG fora + `nosniff` + `Content-Type` sempre um dos da allowlist.
- Em rota autenticada que serve arquivo, o `mime_type` devolvido vem do que foi reconhecido no upload, nunca do que o cliente declarou.

## 4. Quando reavaliar

Upload de novo tipo (PDF, documento, vídeo) exige o mesmo raciocínio: whitelist, parser de
estrutura, limites, metadado (PDF também carrega autor/software), e onde é servido.
