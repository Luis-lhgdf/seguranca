# OWASP ASVS v5.0.0: nível-alvo, mapeamento e gaps

> **Revisado em:** 2026-10-07 · **Origem:** conteúdo compilado de fontes públicas (OWASP, ASVS, NIST, CWE, documentação oficial, avisos de CVE e artigos técnicos) — ver [referências](referencias-gerais.md). Se a data estiver antiga (> 6 meses) ou o tema envolver versão/preço/CVE, confirme na fonte oficial antes de aplicar.

> Fonte: **OWASP ASVS v5.0.0** (release 2025-05-30), numeração `<capítulo>.<seção>.<requisito>`.
> ⚠️ A v5.0.0 **reestruturou** a numeração da v4.x (ex.: Autorização é **V8**, não V4; API/Web
> Service é **V4**). Os IDs abaixo foram conferidos no CSV oficial (`github.com/OWASP/ASVS`,
> tag `v5.0.0`). Ao citar um ID novo, conferir na fonte.

## 1. Como escolher o nível

- **L1** — linha de base, baixa criticidade. Insuficiente para qualquer sistema com dado
  sensível (saúde), dinheiro, MFA ou trilha de auditoria significativa.
- **L2 — piso padrão** para toda aplicação com login e dado pessoal.
- **L3 — só onde o risco se concentra.** Aplicar L3 inteiro num projeto pequeno gera itens
  permanentemente vermelhos (four-eyes com um operador só é "teatro de conformidade").

| Cenário | L3 aplicado em | Gatilho |
|---|---|---|
| Loja virtual com pagamento e dado de saúde | checkout, webhook do gateway, emissão/resgate de voucher, dado clínico | dinheiro + saúde |
| Site institucional + CMS com fotos de pacientes | trilha da imagem de paciente: upload → termo → publicação → entrega → backup | LGPD art. 11 |

**O que o L3 exige a mais, relevante para esses fluxos:**

- **V2.3.5** — aprovação de múltiplos usuários em operação de alto valor (reembolso, emissão manual).
- **V15.4.2** — checagem de estado + ação como operação atômica única (TOCTOU).
- **V4.1.5** — assinatura digital por mensagem em transação altamente sensível (confirmação de pagamento).
- **V8.3.2 / V8.3.3** — mudança de autorização aplicada imediatamente; ação baseada na permissão do sujeito original.
- **V14.2.7** — retenção/exclusão automática de dado sensível por cronograma.
- **V6.3.5 / V6.3.6 / V6.3.7** — notificar tentativa suspeita; e-mail nunca como único/segundo fator; notificar mudança de credencial.
- **V13.1.2 / V13.1.4** — limite documentado de conexões por serviço externo; segredos críticos com rotação obrigatória.
- **V1.2.10** — proteção contra CSV/Formula Injection em exportação.
- Controles de L3 que valem para dado de saúde mesmo em projeto pequeno: retenção/expurgo, proteção em repouso **fora da aplicação** (backup cifrado), log de **acesso** (não só de alteração), segundo fator na conta que administra o dado.

## 2. Mapeamento vulnerabilidade → ASVS

| Item ([fundamentos/vulnerabilidades](../fundamentos/vulnerabilidades.md)) | ASVS v5.0.0 | Nível | O que exige |
|---|---|---|---|
| V01 Webhook forjado/replay | V2.3.4 + V4.1.5 | L2/L3 | locking contra duplo processamento; assinatura por mensagem |
| V02 Race condition | V15.4.2 + V2.3.4 | L3/L2 | estado + ação atômicos |
| V03 Confiar no frontend | V2.2.2 + V8.3.1 | L1 | validação e autorização em camada confiável |
| V04 IDOR | V8.2.1 + V8.2.2 | L1 | acesso por função e por dado restrito a permissão explícita |
| V05 Exposição na resposta | V15.3.1 | L1 | só o subconjunto necessário de campos |
| V06 Mass assignment | V15.3.3 | L2 | campos permitidos por controller/action |
| V07 Autenticação fraca | V6.1.1 + V6.3.1 + V11.4.2 | L1/L1/L2 | anti-automação documentada; KDF aprovada |
| V08 Sessão | V7.2.3 + V3.3.1/3.3.2/3.3.4 | L1/L1-L2 | token CSPRNG ≥ 128 bits; cookie `Secure`/`__Host-`, `SameSite`, `HttpOnly` |
| V09 SQLi | V1.2.4 | L1 | queries parametrizadas/ORM |
| V10 XSS | V1.2.1 + V1.3.1 + V3.2.1/3.2.2 | L1 | encoding contextual; HTML não confiável sanitizado |
| V11 CSRF | V3.5.1 + V3.5.2 + V3.5.3 | L1 | origem validada; funções sensíveis não usam GET |
| V12 Upload | V5.2.2 + V5.3.1 + V5.3.2 | L1 | extensão × conteúdo; não executar; path gerado internamente |
| V13 Rate limit | V2.4.1 + V6.1.1/6.3.1 | L2/L1 | anti-automação |
| V14 Segredos | V13.3.1 + V13.2.3 + V13.3.4 | L2/L2/L3 | cofre; credencial nunca default; rotação |
| V15 Dependências | V15.1.1 + V15.2.1 + V15.1.2 | L1/L1/L2 | prazo de remediação; SBOM |
| V16 Misconfiguration | V13.4.1–V13.4.4 + V3.4.1/V3.4.4 | L1-L2 | sem `.git` exposto; debug off; sem listing/TRACE; HSTS; `nosniff` |
| V17 Logs | V16.2.1 + V16.3.1 + V16.3.2 | L2 | quando/onde/quem/o quê; toda falha de autenticação/autorização logada |
| V18 SSRF | V1.3.6 | L2 | allowlist de protocolo/domínio/porta |
| V23 Classificação/retenção | V14.1.1/V14.1.2 + V14.2.7 | L2/L3 | dado classificado; expurgo por cronograma |
| V24 Cache/Referer/storage | V3.4.5 + V14.3.2 + V14.3.3 | L2 | `Referrer-Policy`; `no-store`; nada sensível em storage |
| Reset sem contornar MFA | V6.4.3 | L2 | reset não pula o segundo fator |
| Reautenticação para mudar e-mail/telefone/MFA | V7.5.1 | L2 | reautenticação completa |
| Código fora de banda | V6.6.1 / V6.6.3 | L2 | OTP só para número já validado; rate limit; considerar ≥ 64 bits de entropia |
| Fator perdido | V6.4.4 | L2 | prova de identidade no mesmo nível do cadastro |
| Não enumerar usuário | V6.3.8 | L3 | cadastro e "esqueci a senha" também |
| Comunicação entre serviços | V13.1.1 + V13.2.1 + V13.2.2 | L2 | necessidades documentadas; conta de serviço/token curto; privilégio mínimo |

## 3. Visão por capítulo (como avaliar um projeto)

| Capítulo | Pergunta-chave |
|---|---|
| V1 Encoding e sanitização | existe algum sink sem escape (JSON-LD, `href`, e-mail HTML, PDF, CSV)? SQL textual? |
| V2 Validação e lógica de negócio | regras de compliance/valor no servidor? operações atômicas? |
| V3 Frontend web | CSP no HTML? cookies corretos? CSRF? Referrer-Policy? nada em `localStorage`? |
| V4 API | CORS sem `*`? schema em toda entrada? `/docs` off? teto de corpo? webhook assinado? |
| V5 Arquivos | magic bytes, allowlist, SVG fora, bomba, metadado, path traversal, privado fora do Nginx? |
| V6 Autenticação | Argon2id+pepper, lockout, rate limit, anti-enumeração, **MFA**, senha vazada, aviso de troca? |
| V7 Sessão | TTL, rotação, reuso, revogação, step-up? |
| V8 Autorização | dono do recurso / módulo+ação relido do banco? recurso mais sensível com permissão própria? |
| V9 Tokens autocontidos | `algorithms` fixo (sem alg confusion), `exp`/`iat`/`type`, segredo forte? |
| V10 OAuth/OIDC | só se houver login social: `email_verified` confiável? não vincular por e-mail? |
| V11 Criptografia | KDF aprovada, CSPRNG, comparação em tempo constante, dado em repouso fora do banco cifrado? |
| V12 Comunicação | TLS 1.2/1.3, HSTS, banco em loopback/rede interna? |
| V13 Configuração | segredos fora do git e do ambiente do contêiner, validador anti-placeholder, CI com gates? |
| V14 Proteção de dados | classificação, retenção, `no-store`, backup cifrado, PII fora de rota pública? |
| V15 Código seguro | SAST, testes rodando no CI, SBOM, prazo de remediação? |
| V16 Logging | autenticação auditada? delete auditado? valor antes/depois? alerta? |
| V17 WebRTC | só se houver mídia em tempo real |

## 4. Gaps recorrentes (achados típicos em auditoria)

1. **SSRF** — esquecido quando há chamada de saída com URL de fora (V18).
2. **Classificação formal de dado** e **retenção/expurgo** — tratado "por convenção" espalhada no código (V23).
3. **Cadeia contra account takeover** — reautenticação para trocar telefone/e-mail/MFA, reset que não pula MFA, notificação de mudança de credencial, step-up em aparelho novo.
4. **Cache/`Referer`/storage** — falta `no-store` em resposta com PII (V24).
5. **Aprovação dupla** em operação de alto valor — com um operador só, o controle compensatório é auditoria com valor antes/depois + restringir a flag a superuser. Quando houver sistema consumidor (SAC/financeiro), a aprovação dupla mora nele.
6. **Comunicação inter-serviços** documentada (destino, credencial, privilégio) e credencial estática migrada para token curto quando possível.
7. **CSP ausente no HTML** com CSP só na API JSON (que não executa script).
8. **CI sem gate** — e `.gitignore` ignorando `.github` (workflow novo descartado em silêncio pelo `git add`).
9. **Backup em claro** carregando dado sensível, no mesmo host.
10. **Trilha de auditoria cega** para login/falha/lockout/reuso de refresh e para `delete`.
