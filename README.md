# RepoHealth CLI

## 1. Membros do grupo

- Guilherme Henrique Gomes Evangelista
- Pedro Bacelar Rigueira
- Caio Souza Grossi
- Ana Paula Pereira Theobald

## 2. Explicação do sistema

O **RepoHealth CLI** é uma ferramenta de linha de comando voltada para a identificação de possíveis problemas de manutenção em projetos de software a partir da mineração de repositórios.

A ideia principal do sistema é analisar dados históricos e estruturais de um repositório, como commits, arquivos modificados, complexidade do código, frequência de alterações e possíveis sinais de acúmulo de dívida técnica. A partir dessas informações, a ferramenta gera um diagnóstico sobre pontos do projeto que podem exigir maior atenção da equipe de desenvolvimento.

Entre os problemas que o sistema pretende identificar estão:

- **Arquivos com alta frequência de mudanças**, que podem indicar instabilidade ou concentração excessiva de manutenção;
- **Arquivos complexos e muito modificados**, que representam maior risco de defeitos e dificuldade de evolução;
- **Trechos com possíveis code smells**, como métodos longos, alta complexidade ciclomática ou excesso de responsabilidades;
- **Arquivos pouco testados ou com baixa presença de testes relacionados**;
- **Pontos críticos do projeto**, combinando métricas de código e histórico de evolução.

A ferramenta poderá receber como entrada a URL de um repositório GitHub ou o caminho de um repositório local. Após a análise, o sistema apresentará um relatório no terminal com os principais problemas encontrados, rankings de arquivos críticos e métricas que ajudem a equipe a priorizar atividades de refatoração e manutenção.

Exemplo de uso esperado:

```bash
repohealth analyze https://github.com/usuario/projeto
