# Tá certo o site?

Projeto web simples para ajudar pessoas não técnicas a comparar um endereço recebido com os domínios oficiais cadastrados de marcas conhecidas.

O sistema não afirma que um site é seguro. Ele informa apenas se o domínio informado corresponde ou não ao domínio oficial cadastrado para a marca selecionada.

## Arquitetura

- `backend/`: API HTTP em Python, organizada em MVC e retornando apenas JSON.
- `docs/`: página estática em HTML, CSS e JavaScript vanilla, pronta para GitHub Pages.
- O backend não renderiza HTML e não depende dos arquivos do frontend.
- O frontend consome o backend apenas por chamadas HTTP.

## Como Rodar o Backend

```bash
cd backend
poetry install
poetry run uvicorn app.main:app --reload
```

A API ficará disponível em `http://localhost:8000`.

Para rodar em modo produção e desabilitar `/docs`, `/redoc` e `/openapi.json`:

```bash
APP_ENV=production poetry run uvicorn app.main:app
```

## Deploy no Render

Configuração recomendada para o backend no Render:

- `Language`: Python 3
- `Branch`: `main`
- `Root Directory`: `backend`
- `Build Command`: `poetry install`
- `Start Command`: `poetry run uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- `Environment Variable`: `APP_ENV=production`

URL pública configurada no frontend:

```js
const API_BASE_URL = "https://tacertoosite.onrender.com";
```

## CORS

As origens permitidas ficam em `backend/app/main.py`, na constante `CORS_ALLOWED_ORIGINS`.

Em desenvolvimento, a API pode ficar aberta:

```python
# "*",
```

A origem pública atual do GitHub Pages já está configurada:

```python
"https://guedeira.github.io",
```

## Como Abrir o Frontend

Abra o arquivo `docs/index.html` no navegador.

Em produção, o frontend chama `https://tacertoosite.onrender.com`.

Para desenvolvimento local, ajuste temporariamente `API_BASE_URL` em `docs/app.js` para `http://localhost:8000`.

## Solicitação de Novas Empresas

O frontend tem um formulário para solicitar a adição de novas empresas e domínios. Ele abre uma issue pré-preenchida no GitHub para revisão manual.

A URL do repositório para abrir issues está configurada em `docs/app.js`:

```js
const GITHUB_NEW_ISSUE_URL = "https://github.com/guedeira/tacertoosite/issues/new";
```

## Rotas

- `GET /brands`: lista marcas disponíveis.
- `GET /brands/{brand_id}`: retorna detalhes de uma marca.
- `GET /health`: verifica se a API está ativa.
- `POST /validate-domain`: compara o domínio informado com os domínios oficiais cadastrados.

No frontend, a página chama `/health` ao abrir. Em hospedagens gratuitas como Render, essa chamada ajuda a acordar o serviço quando ele ficou inativo e mostra uma mensagem enquanto a API inicializa.

Exemplo de payload:

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

## Testes

```bash
cd backend
poetry run python -m unittest discover -s tests
```

## Limitações

- Os domínios oficiais são cadastrados manualmente em `backend/app/data/brands.json`.
- Não há consulta externa, reputação de site, certificado, DNS ou blacklist.
- O resultado não deve ser interpretado como garantia de segurança.
- Subdomínios não são tratados como equivalentes ao domínio oficial nesta versão.
