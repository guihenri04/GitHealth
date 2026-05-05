# RepoHealth CLI

## 1. Membros do grupo

- Guilherme Henrique Gomes Evangelista
- Pedro Bacelar Rigueira
- Caio Souza Grossi
- Ana Paula Pereira Theobald

## 2. Explicação do sistema

O **RepoHealth CLI** é uma ferramenta de linha de comando voltada para identificar possíveis problemas de manutenção em repositórios GitHub por meio da mineração de repositórios de software.

A proposta do sistema é analisar o histórico do projeto e alguns sinais estruturais do código para apontar arquivos, trechos e padrões que merecem mais atenção da equipe. Entre os indícios que podem ser investigados estão arquivos que mudam com muita frequência, componentes que aparecem modificados em conjunto e pontos do repositório que concentram alterações ao longo do tempo.

A ideia é transformar essas informações em um diagnóstico prático, apresentado em forma de relatório com métricas e ranking de itens mais críticos. Esse relatório deve ajudar a priorizar refatorações, entender melhor a evolução do projeto e levantar hipóteses sobre possíveis áreas com acúmulo de dívida técnica.

Além da análise histórica, o sistema também pode evoluir para representar o repositório como um grafo de merges e explorar características associadas a cada mudança, como o tipo de commit ou o contexto da alteração. Essas possibilidades ampliam a capacidade de mineração, mas ainda devem ser tratadas como caminhos de implementação, não como decisões fechadas.

## 3. Possíveis tecnologias utilizadas

O projeto será implementado em **Python** para automação, análise de dados e integração com bibliotecas de mineração de software.

Para a mineração do repositório e acesso ao histórico do Git, uma possibilidade é usar o **PyDriller**, que facilita a extração de commits, arquivos modificados e metadados do repositório. Se houver necessidade de integração mais direta com a API do GitHub, o **PyGithub** também pode ser considerado.

Na parte de linha de comando, ferramentas como **Typer**, **Click** ou **argparse** podem ser usadas para construir uma interface simples e objetiva. Para apoiar a análise dos dados, também podem entrar bibliotecas voltadas a mineração de dados e, se o projeto evoluir para visualizações, soluções para grafos e representação visual das relações entre commits e merges.

Essas tecnologias representam um conjunto de possibilidades compatíveis com a proposta do trabalho e podem ser ajustadas conforme a solução avance.
