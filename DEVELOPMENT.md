# Guia de Desenvolvimento

Este documento reúne as instruções práticas para instalar, executar, testar e manter o projeto localmente.

## Requisitos

- Python 3.12 ou superior.
- Poetry.
- Navegador moderno para abrir o frontend estático.

## Arquitetura

- `backend/`: API HTTP em Python, organizada em camadas e retornando apenas JSON.
- `docs/`: página estática em HTML, CSS e JavaScript vanilla, pronta para GitHub Pages.
- O backend não renderiza HTML e não depende dos arquivos do frontend.
- O frontend consome o backend apenas por chamadas HTTP.

## Instalação do Backend

```bash
cd backend
poetry install
```

## Executando o Backend

```bash
cd backend
poetry run uvicorn app.main:app --reload
```

A API ficará disponível em `http://localhost:8000`.

Em modo de produção, `/docs`, `/redoc` e `/openapi.json` são desabilitados:

```bash
APP_ENV=production poetry run uvicorn app.main:app
```

## Abrindo o Frontend

Abra o arquivo `docs/index.html` no navegador.

Em produção, o frontend chama:

```js
const API_BASE_URL = "https://tacertoosite.onrender.com";
```

Para desenvolvimento local, ajuste temporariamente `API_BASE_URL` em `docs/app.js`:

```js
const API_BASE_URL = "http://localhost:8000";
```

Antes de commitar, volte a URL para o endpoint público caso a alteração local não faça parte da mudança proposta.

## Testes

```bash
cd backend
poetry run python -m unittest discover -s tests
```

Os testes atuais cobrem principalmente:

- normalização de domínios;
- validação de domínios oficiais;
- configuração de segurança do backend.

## Rotas da API

- `GET /brands`: lista marcas disponíveis.
- `GET /brands/{brand_id}`: retorna detalhes de uma marca.
- `GET /health`: verifica se a API está ativa.
- `POST /validate-domain`: compara o domínio informado com os domínios oficiais cadastrados.

Exemplo de payload para `POST /validate-domain`:

```json
{
  "brand_id": "mercado_livre",
  "input": "https://mercadoIivre.com.br/promocao"
}
```

Exemplo de resposta:

```json
{
  "is_match": false,
  "brand": "Mercado Livre",
  "official_domains": ["mercadolivre.com.br"],
  "submitted_domain": "mercadoiivre.com.br",
  "message": "O endereço informado não corresponde ao domínio oficial cadastrado para Mercado Livre."
}
```

## Cadastro de Marcas

Os domínios oficiais ficam em:

```text
backend/app/data/brands.json
```

Ao adicionar ou alterar uma marca:

- use um `id` estável, em minúsculas, sem espaços;
- mantenha o nome legível em `name`;
- cadastre apenas domínios oficiais confirmados;
- prefira fontes oficiais da própria marca;
- adicione ou ajuste testes quando a mudança envolver regra de normalização ou validação.

O frontend também possui um formulário para solicitar novas empresas. Ele abre uma issue pré-preenchida no GitHub para revisão manual.

A URL do repositório para abrir issues está configurada em `docs/app.js`:

```js
const GITHUB_NEW_ISSUE_URL = "https://github.com/guedeira/tacertoosite/issues/new";
```

## CORS

As origens permitidas ficam em `backend/app/main.py`, na constante `CORS_ALLOWED_ORIGINS`.

A origem pública atual do GitHub Pages já está configurada:

```python
"https://guedeira.github.io",
```

Para testar o frontend em servidor local, há origens comentadas no mesmo arquivo:

```python
# "http://localhost:5500",
# "http://127.0.0.1:5500",
```

Se precisar depurar CORS localmente, a API pode ser aberta temporariamente:

```python
# "*",
```

Não deixe `*` habilitado em produção.

## Deploy no Render

Configuração recomendada para o backend no Render:

- `Language`: Python 3.
- `Branch`: `main`.
- `Root Directory`: `backend`.
- `Build Command`: `poetry install`.
- `Start Command`: `poetry run uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
- `Environment Variable`: `APP_ENV=production`.

## Convenções

- Backend em Python com FastAPI.
- Frontend em HTML, CSS e JavaScript vanilla.
- Respostas da API sempre em JSON.
- Nomes de arquivos e identificadores técnicos em inglês quando já seguirem o padrão do código.
- Textos para usuários em português.
- Mudanças devem ser pequenas, focadas e acompanhadas de testes quando alterarem comportamento.
- O backend e o frontend devem permanecer desacoplados: o backend não deve renderizar páginas do `docs/`.

## Segurança e Escopo

O projeto compara domínios cadastrados manualmente. Ele não deve apresentar o resultado como uma garantia de segurança.

Evite mensagens definitivas como "site seguro" ou "site falso". Prefira linguagem objetiva, como:

- "corresponde ao domínio oficial cadastrado";
- "não corresponde ao domínio oficial cadastrado";
- "verifique também outros sinais antes de informar dados pessoais".
