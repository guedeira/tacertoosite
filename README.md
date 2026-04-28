# Tá certo o site?

Uma ferramenta simples para ajudar pessoas a conferir se um endereço recebido corresponde ao domínio oficial cadastrado de uma empresa conhecida.

O projeto nasceu de um problema cotidiano: golpes usam links parecidos com os de empresas legítimas para confundir pessoas e capturar dados. O **Tá certo o site?** não promete dizer se um site é seguro, mas ajuda a responder uma pergunta mais objetiva: "esse domínio é o domínio oficial cadastrado para essa empresa?"

## Como Funciona

1. A pessoa escolhe uma empresa na interface.
2. Informa o endereço que recebeu.
3. O sistema normaliza o domínio informado e compara com os domínios oficiais cadastrados manualmente.
4. A resposta informa se houve correspondência ou não.

O resultado deve ser tratado como apoio à verificação, não como garantia de segurança.

## Principais Recursos

- Comparação de domínios informados com domínios oficiais cadastrados.
- Normalização de URLs para reduzir erros comuns de digitação e formato.
- Frontend estático em HTML, CSS e JavaScript vanilla.
- API HTTP em Python com FastAPI.
- Formulário para solicitar a inclusão de novas empresas por issue no GitHub.

## Limitações

- Os domínios oficiais são cadastrados manualmente em `backend/app/data/brands.json`.
- O sistema não consulta reputação, certificado, DNS, blacklist ou bases externas.
- Um resultado positivo não garante que uma página seja segura.
- Um resultado negativo indica apenas que o domínio não corresponde ao cadastro atual.
- Subdomínios não são tratados como equivalentes ao domínio oficial nesta versão.

## Roadmap

- Integrar ferramentas externas para consultar a reputação do domínio analisado:
  - Google Safe Browsing;
  - AlienVault OTX;
  - AbuseIPDB;
  - VirusTotal;
  - URLhaus;
  - isMalicious;
  - alphaMountain;
  - Shodan;
  - Web of Trust.
- Implementar banco de dados para armazenar empresas cadastradas, resultados de integrações e histórico de análises.
- Criar painel de reputação global e por empresa.
- Criar um checklist antigolpe para ajudar pessoas não técnicas a avaliar sinais de risco:
  - domínio conferido no Tá certo o site?;
  - link recebido por mensagem suspeita?;
  - presença de urgência ou pressão?;
  - existência de redirecionamento?;
  - acesso possível pelo site oficial?.
- Criar vídeos curtos de conscientização para pessoas não técnicas:
  - como identificar a URL e o domínio;
  - sinais comuns de golpe;
  - golpes por WhatsApp, Telegram e outros canais;
  - como verificar um link antes de clicar.
- Criar um score de reputação interno, cruzando sinais como volume de consultas e histórico de análises.
- Melhorar a experiência do frontend.
- Padronizar nomes internos (vars) do frontend e backend de `brand` para `company`, acompanhando a linguagem exibida ao usuário.

## Como Rodar

As instruções completas de instalação, execução local, deploy e convenções estão em [DEVELOPMENT.md](./DEVELOPMENT.md).

Resumo rápido:

```bash
cd backend
poetry install
poetry run uvicorn app.main:app --reload
```

Depois, abra `docs/index.html` no navegador. Para usar a API local, ajuste temporariamente `API_BASE_URL` em `docs/app.js` para `http://localhost:8000`.

## Como Contribuir

Contribuições são bem-vindas, especialmente em:

- cadastro ou correção de empresas e domínios oficiais;
- melhorias de acessibilidade e clareza na interface;
- testes para validação e normalização de domínios;
- melhorias de documentação;
- correções de segurança e confiabilidade.

Antes de abrir um pull request:

1. Rode os testes do backend.
2. Mantenha mudanças pequenas e focadas.
3. Explique a motivação da alteração.
4. Para novas empresas, inclua uma fonte confiável que comprove o domínio oficial.

Também é possível solicitar uma nova empresa diretamente pela interface, que abre uma issue pré-preenchida para revisão manual.

## Desenvolvimento

Consulte [DEVELOPMENT.md](./DEVELOPMENT.md) para:

- requisitos locais;
- comandos de instalação e testes;
- arquitetura;
- rotas da API;
- configuração de CORS;
- deploy no Render;
- convenções do projeto.

## Licença

Este projeto está licenciado sob a licença MIT. Consulte [LICENSE.md](./LICENSE.md) para mais detalhes.
