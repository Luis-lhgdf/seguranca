# Operação: resposta a incidente, contas externas e pessoas

> **Revisado em:** 2026-10-07 · **Origem:** conteúdo compilado de fontes públicas (OWASP, ASVS, NIST, CWE, documentação oficial, avisos de CVE e artigos técnicos) — ver [referências](referencias.md). Prazos legais mudam: conferir a regra vigente da ANPD.

## 1. Plano de resposta a incidente (runbook)

Escrito **antes** do incidente — improvisar no dia é o pior cenário. Mínimo:
1. **Quem** é avisado (responsável técnico, dono do negócio, DPO/encarregado, jurídico) e por qual canal.
2. **Conter:** como isolar (tirar do ar, bloquear acesso ao painel, revogar sessões, rotacionar segredos, trocar chaves de API, snapshot para perícia **antes** de limpar).
3. **Avaliar:** que dado, de quantos titulares, desde quando (trilha de auditoria, logs do Nginx, `uploads.log`, logins SSH).
4. **Comunicar:** ANPD e titulares quando houver risco ou dano relevante — prazo definido no regulamento da ANPD (Res. CD/ANPD nº 15/2024: **3 dias úteis**, conferir a vigente); texto-modelo pronto.
5. **Recuperar:** restaurar de backup íntegro, corrigir a causa, monitorar.
6. **Aprender:** registro do incidente e do que mudou.

Rollbacks rápidos documentados (ex.: CSP para Report-Only; blue-green para a cor anterior).

## 2. Contas satélites (fora do repositório, mas no perímetro)

MFA e dono definido em: e-mail corporativo e de recuperação, registrador do domínio/DNS,
hospedagem/VPS (painel do provedor), GitHub (e secrets do repositório), CDN/Cloudflare, redes
sociais, portal do gateway, conta Meta/WhatsApp Business, AWS, CMS/ERP externo. Revisão periódica
de quem tem acesso; quem saiu perde o acesso no dia.

## 3. Pessoas

- Treinamento contra **phishing/BEC**; dupla verificação fora de banda para pagamento e mudança bancária.
- Combinado público do que a empresa **nunca** pede (ex.: sinal por WhatsApp) — golpe de terceiro queima a marca.
- Operador único: senha exclusiva do painel; desconfiar de link pedindo relogin; nunca colar `.env`/token/chave em chat ou IA.
- Login nominal (sem conta compartilhada).

## 4. Processo de desenvolvimento

- Segurança entra junto com a feature; revisão obrigatória em autenticação, upload, pagamento e dado sensível.
- Teste visto reprovando antes de confiar ("verde nunca visto vermelho não prova nada").
- Documento é hipótese: marcar "feito" só com verificação no código/servidor (caso típico: dois documentos divergem e o desempate só vem da verificação direta).
- Registrar decisões e riscos aceitos com data e responsável.
- Pentest externo recomendado antes de go-live de sistema com dinheiro ou dado sensível.
