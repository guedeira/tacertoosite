# Tá certo o site?

Uma ferramenta simples para ajudar pessoas a conferir se um endereço recebido corresponde ao domínio oficial cadastrado de uma marca conhecida.

O projeto nasceu de um problema cotidiano: golpes usam links parecidos com os de empresas legítimas para confundir pessoas e capturar dados. O **Tá certo o site?** não promete dizer se um site é seguro, mas ajuda a responder uma pergunta mais objetiva: "esse domínio é o domínio oficial cadastrado para essa marca?"

## Como Funciona

1. A pessoa escolhe uma marca na interface.
2. Informa o endereço que recebeu.
3. O sistema normaliza o domínio informado e compara com os domínios oficiais cadastrados manualmente.
4. A resposta informa se houve correspondência ou não.

O resultado deve ser tratado como apoio à verificação, não como garantia de segurança.

## Principais Recursos

- Comparação de domínios informados com domínios oficiais cadastrados.
- Normalização de URLs para reduzir erros comuns de digitação e formato.
- Frontend estático em HTML, CSS e JavaScript vanilla.
- API HTTP em Python com FastAPI.
- Formulário para solicitar a inclusão de novas marcas por issue no GitHub.

## Limitações

- Os domínios oficiais são cadastrados manualmente em `backend/app/data/brands.json`.
- O sistema não consulta reputação, certificado, DNS, blacklist ou bases externas.
- Um resultado positivo não garante que uma página seja segura.
- Um resultado negativo indica apenas que o domínio não corresponde ao cadastro atual.
- Subdomínios não são tratados como equivalentes ao domínio oficial nesta versão.

## Roadmap

- Melhorar mensagens de resultado para orientar próximos passos sem afirmar que um site é seguro.
- Ampliar a base de marcas e domínios oficiais cadastrados.
- Adicionar fontes de referência para cada domínio oficial cadastrado.
- Tratar subdomínios oficiais de forma mais clara.
- Criar filtros, busca ou categorias para facilitar a navegação por marcas.
- Melhorar acessibilidade, responsividade e estados de erro do frontend atual.
- Adicionar mais testes para casos de URL parecida, domínio internacionalizado e entradas malformadas.
- Criar um processo mais estruturado para revisar solicitações de novas marcas.
- Integrar um banco de dados para armazenar marcas, domínios, fontes e solicitações.
- Criar um sistema interno de reputação para domínios, com histórico de análises e sinais próprios.
- Integrar com o VirusTotal para consultar reputação e detecções conhecidas de domínios informados.
- Substituir o frontend estático por uma aplicação mais moderna e escalável.
- Exibir uma análise mais completa combinando domínio oficial, reputação interna, VirusTotal e outros sinais de risco.

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

- cadastro ou correção de marcas e domínios oficiais;
- melhorias de acessibilidade e clareza na interface;
- testes para validação e normalização de domínios;
- melhorias de documentação;
- correções de segurança e confiabilidade.

Antes de abrir um pull request:

1. Rode os testes do backend.
2. Mantenha mudanças pequenas e focadas.
3. Explique a motivação da alteração.
4. Para novas marcas, inclua uma fonte confiável que comprove o domínio oficial.

Também é possível solicitar uma nova marca diretamente pela interface, que abre uma issue pré-preenchida para revisão manual.

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
