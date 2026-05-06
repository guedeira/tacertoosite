# Desenvolvimento

Guia rápido para rodar, testar e mexer no projeto.

## Stack

- `backend/`: FastAPI, Python 3.12+, `uv`.
- `frontend/`: Vue 3, Vite, TypeScript, npm.
- `docs/`: build estático gerado pelo frontend.

O produto compara o domínio registrável principal informado pela pessoa usuária com os domínios oficiais em `backend/app/data/brands.json`.

## Rodar Localmente

Backend:

```bash
cd backend
uv sync
uv run uvicorn app.main:app --reload
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

Build estático:

```bash
cd frontend
npm run build
```

O Vite usa proxy em `/api` no desenvolvimento. Em produção, o frontend usa `VITE_API_BASE_URL` ou `https://tacertoosite.onrender.com`.

## Testes

Backend:

```bash
cd backend
uv run python -m unittest discover
```

Frontend:

```bash
cd frontend
npm run typecheck
npm test
```

Rode testes ao mexer em normalização/validação de domínio, cadastro de empresas, serviços HTTP ou estados importantes da interface.

## Backend

Estrutura:

- `routes`: rotas FastAPI.
- `controllers`: adaptação HTTP para serviços.
- `services`: regras de negócio.
- `repositories`: leitura de dados.
- `models`: estruturas de domínio.
- `data`: cadastro manual.

Regras:

- Regra de negócio fica em `services`.
- Leitura de arquivo fica em `repositories`.
- Models não devem depender de FastAPI.
- Use imports absolutos a partir de `app`.
- Mantenha dependências em `backend/pyproject.toml`; rode `uv lock` após alterar.

## Frontend

Estrutura principal:

- `src/components`: componentes.
- `src/pages`: páginas.
- `src/services`: HTTP.
- `src/types`: tipos compartilhados.
- `src/styles/main.css`: CSS global.

Cuidados:

- Preserve acessibilidade básica: labels, foco, `aria-live` e mensagens claras.
- Não use `v-html` com conteúdo vindo de usuário/API.
- Teste estados de erro, carregamento, vazio, sucesso e alerta.

## Cadastro

Arquivo: `backend/app/data/brands.json`.

Padrão:

- `id`: minúsculo, `snake_case`.
- `name`: nome público.
- `official_domains`: domínios em minúsculas, sem protocolo, caminho ou barra final.

Exemplo:

```json
{
  "id": "mercado_livre",
  "name": "Mercado Livre",
  "official_domains": ["mercadolivre.com.br", "mercadolibre.com"]
}
```

Antes de adicionar domínio, confirme em fonte oficial.

## Convenções

- Código interno em inglês; texto da interface em português.
- Python: `snake_case` para arquivos/funções, `PascalCase` para classes.
- TypeScript/Vue: `camelCase` para variáveis, `PascalCase` para tipos/componentes.
- CSS: classes em `kebab-case`.
- JSON: chaves em `snake_case`.
- O código ainda usa `brand`; não misture com `company` sem migração completa.

## Segurança

- Trate todo link informado como entrada não confiável.
- Normalize antes de comparar.
- Compare pelo domínio registrável principal, não pelo host completo.
- Não execute, acesse ou siga links recebidos no backend.
- Não prometa detectar golpe ou garantir segurança: o resultado é apenas apoio à verificação.
- Em produção, docs da API ficam desativadas com `APP_ENV=production`.

## Git

- `main`: produção.
- `dev`: integração.
- Branches de trabalho saem de `dev`.
- PRs devem ir para `dev`.

Antes de abrir PR:

- rode os testes relevantes;
- mantenha a mudança pequena;
- revise configuração local;
- explique o motivo da alteração.
