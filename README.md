# GitHealth CLI

## 1. Membros do grupo

- Guilherme Henrique Gomes Evangelista
- Pedro Bacelar Rigueira
- Caio Souza Grossi
- Ana Paula Pereira Theobald

## 2. Explicação do sistema

O **GitHealth CLI** é uma ferramenta de linha de comando voltada para identificar possíveis problemas de manutenção em repositórios GitHub por meio da mineração de repositórios de software.

A proposta do sistema é analisar o histórico de evolução de um projeto e extrair informações que ajudem a compreender quais partes do código podem exigir mais atenção da equipe de desenvolvimento. A ferramenta poderá receber como entrada a URL de um repositório GitHub ou o caminho de um repositório local e, a partir disso, coletar dados sobre commits, arquivos modificados, frequência de alterações e relações entre mudanças.

Entre os indícios que podem ser investigados estão arquivos que mudam com muita frequência, arquivos que concentram muitas alterações ao longo do tempo, componentes que costumam ser modificados em conjunto e pontos do projeto com maior risco de acúmulo de dívida técnica. Esses sinais podem indicar partes do sistema mais difíceis de manter, mais propensas a erros ou que talvez precisem de refatoração.

A ideia é transformar essas informações em um diagnóstico prático, apresentado em forma de relatório no terminal. Esse relatório poderá conter métricas, rankings de arquivos mais críticos e possíveis alertas sobre padrões encontrados durante a mineração do repositório. Dessa forma, a ferramenta busca apoiar a equipe na priorização de melhorias, refatorações e atividades de manutenção.

Além da análise histórica, o sistema também pode evoluir para representar o repositório como um grafo de commits, merges ou arquivos relacionados. Essa representação permitiria explorar conexões entre mudanças, identificar componentes que evoluem juntos e visualizar melhor a estrutura de manutenção do projeto. Essas possibilidades ampliam a capacidade de análise, mas ainda devem ser tratadas como caminhos de implementação, não como decisões definitivas.

## 3. Possíveis tecnologias utilizadas

O projeto será desenvolvido principalmente em **Python**, por ser uma linguagem adequada para automação, análise de dados, mineração de repositórios e criação de ferramentas de linha de comando.

Para a mineração do repositório e acesso ao histórico do Git, uma possibilidade é utilizar o **PyDriller**, biblioteca que facilita a extração de commits, arquivos modificados, autores, datas e metadados do repositório. Caso seja necessário acessar informações específicas do GitHub, como dados do repositório, issues ou pull requests, o **PyGithub** ou a própria **GitHub API** também podem ser considerados.

Na construção da interface de linha de comando, ferramentas como **Typer**, **Click** ou **argparse** podem ser utilizadas para criar comandos simples e objetivos, como comandos de análise, geração de relatório e exportação de resultados.

Para apoiar o processamento e a organização dos dados minerados, podem ser utilizadas bibliotecas como **Pandas**, que facilita a manipulação de tabelas, métricas e rankings. Para a apresentação dos resultados no terminal, a biblioteca **Rich** pode ser usada para gerar tabelas, mensagens formatadas e uma visualização mais clara das informações.

Caso o projeto avance para uma análise baseada em grafos, a biblioteca **NetworkX** pode ser utilizada para representar relações entre commits, merges, arquivos ou componentes que mudam em conjunto. Também podem ser consideradas bibliotecas de visualização, caso seja necessário gerar gráficos ou imagens para complementar o relatório.

Essas tecnologias representam um conjunto de possibilidades compatíveis com a proposta do trabalho e poderão ser ajustadas conforme a solução for sendo desenvolvida.
