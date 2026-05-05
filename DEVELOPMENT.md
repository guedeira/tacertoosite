# Desenvolvimento

Este documento reúne o que um dev precisa saber para trabalhar no projeto sem precisar garimpar decisões básicas no código. Ele não lista rotas da API de propósito: para isso, consulte os arquivos em `backend/app/routes`.

## Visão Geral

O projeto é dividido em duas partes:

- `backend/`: API em Python com FastAPI.
- `frontend/`: aplicação Vue 3 com Vite e TypeScript.
- `docs/`: build estático gerado pelo Vite e publicado como site estático.

A regra principal do produto é simples: o backend normaliza o domínio informado pela pessoa usuária e compara esse domínio com a lista manual de domínios oficiais cadastrados em `backend/app/data/brands.json`.

O resultado é apoio à verificação, não garantia de segurança. Evite textos, nomes ou mudanças que prometam detectar golpe, validar certificado, consultar reputação ou afirmar que um site é seguro, a menos que essa capacidade exista no código.

## Requisitos

- Python 3.12 ou superior.
- Poetry.
- Node.js e npm para rodar e gerar o frontend.
- Navegador moderno para testar o frontend estático.

## Como Rodar Localmente

Instale e rode o backend:

```bash
cd backend
poetry install
poetry run uvicorn app.main:app --reload
```

Em outro terminal, instale e rode o frontend:

```bash
cd frontend
npm install
npm run dev
```

O Vite usa proxy em `/api` durante o desenvolvimento para evitar mudanças de CORS no backend. Em produção, o frontend usa `VITE_API_BASE_URL` ou, por padrão, `https://tacertoosite.onrender.com`.

Para gerar o build estático publicado em `docs/`:

```bash
cd frontend
npm run build
```

## Testes

Os testes do backend ficam em `backend/tests` e usam `unittest`.

Para rodar o backend:

```bash
cd backend
poetry run python -m unittest discover
```

Os testes do frontend ficam próximos ao código em `frontend/src` e usam Vitest.

Para rodar o frontend:

```bash
cd frontend
npm run typecheck
npm test
```

Adicione ou atualize testes de backend quando mexer em:

- normalização de domínio;
- validação de domínio;
- regras de segurança de entrada;
- estrutura do cadastro de empresas;
- comportamento que altere a resposta esperada pela interface.

Adicione ou atualize testes de frontend quando mexer em:

- filtros e seleção de empresas;
- serviços HTTP;
- estados de resultado, erro e carregamento;
- componentes com regras de interação relevantes.

## Arquitetura do Backend

O backend segue uma separação simples por responsabilidade:

- `routes`: camada HTTP/FastAPI, valida entrada e chama controllers.
- `controllers`: adapta chamadas HTTP para serviços e retorna `dict`.
- `services`: regras de negócio.
- `repositories`: leitura de dados.
- `models`: estruturas de domínio.
- `data`: cadastro manual de empresas e domínios oficiais.
- `utils`: utilitários compartilhados, quando realmente necessários.

Prefira manter essa divisão. Regra de negócio não deve ficar em `routes`; leitura de arquivo não deve ficar em `services`; modelos não devem conhecer FastAPI.

Os modelos atuais usam `dataclass(frozen=True)` para representar dados imutáveis e métodos `to_dict()`/`from_dict()` quando precisam atravessar fronteiras com JSON.

Serviços recebem dependências opcionais no construtor. Esse padrão facilita testes sem frameworks extras de injeção de dependência:

```python
class ExampleService:
    def __init__(self, repository: ExampleRepository | None = None) -> None:
        self.repository = repository or ExampleRepository()
```

## Frontend

O frontend em `frontend/` é organizado com Vue 3, Vite e TypeScript:

- componentes em atomic design (`atoms`, `molecules`, `organisms`, `templates`);
- páginas em `frontend/src/pages`;
- serviços HTTP em `frontend/src/services`;
- tipos compartilhados do frontend em `frontend/src/types`;
- CSS global em `frontend/src/styles/main.css`;
- build estático gerado em `docs/`.

Ao alterar a interface:

- preserve acessibilidade básica: `label`, `aria-live`, `aria-label`, foco em modais e mensagens compreensíveis;
- evite `v-html` para conteúdo vindo de usuário ou API;
- mantenha textos claros para pessoas não técnicas;
- teste estados de erro, carregamento, lista vazia e resultado positivo/negativo;
- rode `npm run typecheck`, `npm test` e `npm run build` antes de publicar mudanças no frontend.

## Cadastro de Empresas

O cadastro fica em `backend/app/data/brands.json`.

Padrões atuais:

- categorias em inglês, no plural ou em nomes compostos com `snake_case`;
- `id` da empresa em inglês ou nome normalizado, sempre em minúsculas e `snake_case`;
- `name` com o nome público da empresa;
- `official_domains` como lista de domínios em minúsculas, sem protocolo, sem caminho e sem barra final.

Exemplo:

```json
{
  "id": "mercado_livre",
  "name": "Mercado Livre",
  "official_domains": ["mercadolivre.com.br", "mercadolibre.com"]
}
```

Antes de adicionar uma empresa, valide a fonte oficial. Não cadastre domínio sugerido por e-mail, anúncio, mensagem de terceiros ou página suspeita sem confirmação confiável.

## Convenções de Código

Use nomes internos em inglês. A interface e mensagens para pessoas usuárias podem ficar em português.

Python:

- arquivos e módulos em `snake_case`;
- variáveis, funções e métodos em `snake_case`;
- classes em `PascalCase`;
- constantes em `UPPER_SNAKE_CASE`;
- type hints em código novo;
- retornos explícitos e simples;
- imports absolutos a partir de `app`;
- prefira biblioteca padrão quando ela resolver bem o problema.

TypeScript/Vue:

- arquivos de componentes em `PascalCase.vue`;
- variáveis, funções, refs e computeds em `camelCase`;
- tipos e interfaces em `PascalCase`;
- serviços HTTP isolados em `frontend/src/services`;
- tipos compartilhados em `frontend/src/types`;
- constantes globais de configuração em `UPPER_SNAKE_CASE`;
- use `const` por padrão e `let` apenas quando o valor muda;
- prefira props e emits tipados em componentes novos.

HTML/CSS:

- classes CSS em `kebab-case`;
- ids em `kebab-case`;
- mantenha estrutura semântica (`header`, `main`, `section`, `aside`, `footer`, `dialog`);
- prefira classes descritivas ao invés de estilos acoplados ao conteúdo.

JSON:

- chaves em `snake_case`;
- strings de domínio em minúsculas;
- listas ordenadas de forma legível para revisão humana.

## Padrões de Nomenclatura do Domínio

O código ainda usa `brand` para representar empresas cadastradas. O README cita a intenção futura de padronizar nomes internos de `brand` para `company`.

Enquanto essa migração não acontecer, mantenha consistência com o código existente:

- use `brand` em variáveis, classes e payloads que interagem com o código atual;
- use "empresa" nos textos da interface;
- não misture `brand` e `company` na mesma mudança sem fazer uma migração completa e testada.

## Segurança e Validação

Este projeto lida com links potencialmente suspeitos, então mantenha as entradas tratadas como não confiáveis.

Cuidados esperados:

- validar tamanho e formato de entrada na camada HTTP quando fizer sentido;
- normalizar antes de comparar domínios;
- não tratar subdomínios como equivalentes automaticamente;
- não executar, seguir ou abrir links informados pela pessoa usuária no backend;
- escapar conteúdo dinâmico no frontend;
- manter documentação interativa da API desativada em produção via `APP_ENV=production`;
- manter CORS restrito às origens necessárias.

## Fluxo Git

O repositório tem branches `main` e `dev`. O fluxo recomendado é uma variação simples de Gitflow:

- `main`: código estável/de produção.
- `dev`: integração das próximas mudanças.
- branches de trabalho: criadas a partir de `dev`.
- pull requests: sempre da branch de trabalho para `dev`.

Não commite diretamente em `main` ou `dev`.

Sugestão de nomes:

```bash
feature/nome-curto
fix/nome-curto
docs/nome-curto
chore/nome-curto
```

Fluxo básico:

```bash
git checkout dev
git pull
git checkout -b docs/atualiza-development
```

Antes de abrir PR:

- rode os testes relevantes;
- revise se não ficou configuração local commitada;
- mantenha o PR pequeno e focado;
- descreva o motivo da mudança;
- para novas empresas, inclua a fonte usada para confirmar o domínio oficial.

Quando uma versão estiver pronta, a promoção de `dev` para `main` deve ser feita por PR/release, não por commit direto.

## Antes de Enviar uma Mudança

Checklist rápido:

- A mudança mantém a separação de camadas?
- Nomes internos estão em inglês?
- Python segue `snake_case` e TypeScript segue `camelCase`/`PascalCase` conforme o tipo de símbolo?
- Dados públicos e mensagens para usuários continuam claros em português?
- Entradas externas continuam validadas e escapadas?
- Testes foram adicionados ou atualizados quando a regra mudou?
- O build estático em `docs/` foi atualizado quando o frontend mudou?
- O frontend foi testado manualmente nos fluxos afetados?
- Nenhuma configuração local foi commitada por acidente?
