# GitHealth

GitHealth e uma ferramenta de linha de comando para minerar pull requests de
repositorios GitHub e identificar caracteristicas associadas a revisoes mais
demoradas ou trabalhosas.

## Membros do grupo

- Guilherme Henrique Gomes Evangelista
- Pedro Bacelar Rigueira
- Caio Souza Grossi
- Ana Paula Pereira Theobald

## Objetivo da ferramenta

Equipes de desenvolvimento frequentemente nao sabem quais tipos de pull request
demoram mais para receber revisao, quais caracteristicas aumentam o esforco de
review e quais arquivos aparecem repetidamente em mudancas demoradas.

O GitHealth coleta dados historicos de pull requests fechados ou merged e calcula
metricas como:

- tempo ate a primeira revisao;
- tempo total ate merge ou fechamento;
- tempo depois da primeira revisao;
- quantidade de arquivos modificados;
- quantidade de commits;
- adicoes, remocoes e churn;
- quantidade de reviews;
- pedidos de alteracao;
- comentarios de review;
- arquivos associados a PRs demorados;
- correlacoes de Spearman entre tamanho, esforco e tempo.

A ferramenta apresenta associacoes historicas. Os resultados nao devem ser
interpretados como prova de causalidade.

## Tecnologias utilizadas

- Python 3.12+
- Typer para a interface de linha de comando
- HTTPX para chamadas a API do GitHub
- Dataclasses para os modelos de dados
- Pandas para correlacoes
- Rich para exibicao no terminal
- Jinja2 para gerar HTML
- Plotly para graficos no relatorio
- Pytest para testes
- RESPX e HTTPX MockTransport para testes de HTTP
- Ruff para lint
- GitHub Actions para integracao continua

## Instalacao

Clone o repositorio:

```bash
git clone https://github.com/guihenri04/GitHealth.git
cd GitHealth
```

Crie e ative um ambiente virtual:

```bash
python -m venv .venv
source .venv/bin/activate
```

No Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

Instale a ferramenta:

```bash
pip install -e .
```

Para desenvolvimento, instale tambem as dependencias de teste:

```bash
pip install -e ".[dev]"
```

Configure um token do GitHub:

```bash
export GITHUB_TOKEN="github_pat_seu_token"
```

No Windows PowerShell:

```powershell
$env:GITHUB_TOKEN="github_pat_seu_token"
```

O token nao deve ser passado como argumento da CLI, para evitar que ele fique
salvo no historico do terminal.

## Como utilizar

Verifique a configuracao local:

```bash
githealth doctor
```

Analise um repositorio usando `owner/repository`:

```bash
githealth analyze django/django
```

Tambem e possivel usar a URL completa:

```bash
githealth analyze https://github.com/django/django
```

Defina um intervalo de datas:

```bash
githealth analyze django/django \
  --since 2025-01-01 \
  --until 2026-01-01
```

Escolha a pasta de saida:

```bash
githealth analyze django/django \
  --output ./reports/django
```

Inclua PRs criados por bots:

```bash
githealth analyze django/django --include-bots
```

Limite a quantidade de PRs coletados, util para testes manuais:

```bash
githealth analyze django/django --limit 20
```

Inspecione um unico pull request:

```bash
githealth inspect django/django 12345
```

## Relatorios gerados

Por padrao, a ferramenta exibe um resumo no terminal e gera os arquivos:

```text
reports/
├── summary.html
├── pull_requests.csv
├── file_hotspots.csv
└── analysis.json
```

O relatorio HTML contem graficos, correlacoes, arquivos classificados como
hotspots e pull requests com maior tempo de ciclo.

## Como executar os testes localmente

Instale as dependencias de desenvolvimento:

```bash
pip install -e ".[dev]"
```

Execute os testes:

```bash
pytest
```

Execute os testes com cobertura:

```bash
pytest --cov=githealth --cov-report=term-missing
```

Execute o lint:

```bash
ruff check .
```

## Integracao continua

O projeto usa GitHub Actions para executar lint e testes automaticamente a cada
push na branch `main` e a cada pull request.

O workflow esta em:

```text
.github/workflows/tests.yml
```

## Limitacoes

- A primeira versao suporta apenas repositorios hospedados no GitHub.
- A ferramenta nao tenta detectar automaticamente se uma mudanca foi feita com IA.
- As correlacoes indicam associacoes historicas, nao causalidade.
- Repositorios com poucos pull requests podem gerar resultados pouco representativos.
- O tempo em draft depende da presenca do evento `ready_for_review` na API.

