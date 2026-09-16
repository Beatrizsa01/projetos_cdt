📌 AUTOMAÇÃO DE TAREFAS 📌

Sobre o projeto:

Automação de Tarefas é um sistema desenvolvido em Python para facilitar a criação e o gerenciamento de tarefas.

O sistema recebe uma solicitação escrita pelo usuário e identifica automaticamente informações importantes, como responsável, prazo, prioridade, categoria e status da tarefa.

Exemplo

Uma solicitação como:

O Ivan precisa preparar o relatório para o cliente até sexta. É urgente.

pode ser transformada automaticamente em:

Responsável: Ivan
Prazo: sexta-feira
Prioridade: ALTA
Categoria: DOCUMENTOS
Status: PENDENTE

Objetivo

O objetivo do projeto é automatizar a organização de tarefas, reduzindo a necessidade de preencher manualmente todas as informações de cada tarefa.

⸻

Funcionalidades ⚙

O sistema permite:

* Criar tarefas a partir de solicitações escritas;
* Identificar automaticamente o responsável;
* Identificar o prazo;
* Identificar a prioridade;
* Identificar a categoria;
* Definir o status da tarefa;
* Listar tarefas cadastradas;
* Pesquisar tarefas;
* Concluir tarefas;
* Excluir tarefas;
* Visualizar estatísticas;
* Exportar tarefas para JSON;
* Importar tarefas de arquivos JSON;
* Gerar tarefas fictícias para testes utilizando Faker;
* Armazenar as tarefas em um banco de dados SQLite.

⸻

Versões do projeto

O projeto possui duas versões de utilização.

Interface gráfica

A versão gráfica foi desenvolvida utilizando Tkinter.

Ela possui:

* Dashboard;
* Criação de novas solicitações;
* Lista de tarefas;
* Pesquisa de tarefas;
* Conclusão de tarefas;
* Exclusão de tarefas;
* Estatísticas;
* Importação e exportação de dados;
* Geração de dados de teste com Faker.

Interface CLI

A versão CLI funciona diretamente pelo terminal.

O menu possui as seguintes opções:

1. Nova solicitação
2. Minhas tarefas
3. Concluir tarefa
4. Excluir tarefa
5. Estatísticas
6. Exportar JSON
7. Importar JSON
8. Gerar dados com Faker
9. Sair

⸻

Como funciona 🛠

O funcionamento do sistema segue o seguinte fluxo:

Solicitação escrita
        ↓
Análise do texto
        ↓
Identificação das informações
        ↓
Criação da tarefa
        ↓
Armazenamento no SQLite
        ↓
Visualização e gerenciamento

O sistema utiliza expressões regulares (Regex) e regras de identificação para analisar a solicitação e encontrar as informações necessárias.

⸻

Identificação do responsável

O sistema procura nomes dentro da solicitação e utiliza essa informação para definir o responsável pela tarefa.

Exemplo:

A Beatriz precisa enviar o relatório para o cliente.

Resultado:

Responsável:Beatriz

Caso nenhum responsável seja identificado:

Responsável: Não definido

⸻

Identificação do prazo

O sistema reconhece diferentes formas de informar uma data ou prazo.

Entre elas:

* Hoje;
* Amanhã;
* Dias da semana;
* Datas completas;
* Datas no formato 20/09/2026;
* Datas no formato 20-09-2026;
* Datas como 20/09;
* Expressões como até dia 20;
* Expressões como até sexta;
* Expressões como 20 de setembro.

Caso nenhum prazo seja identificado:

Prazo: Não definido

⸻

Identificação da prioridade

A prioridade é identificada através de palavras presentes na solicitação.

Prioridade alta

Alguns exemplos de palavras utilizadas:

urgente
imediatamente
agora
crítico
pra ontem
o quanto antes

Prioridade média

Alguns exemplos:

importante
prioridade
atenção

Prioridade baixa

Quando nenhuma indicação de prioridade alta ou média é encontrada, a tarefa recebe prioridade:

BAIXA

⸻

Identificação da categoria

O sistema também identifica a categoria da tarefa através de palavras relacionadas ao conteúdo da solicitação.

As categorias utilizadas incluem:

DOCUMENTOS
REUNIÃO
CLIENTE / VENDAS
FINANCEIRO
TECNOLOGIA
GERAL

Caso nenhuma categoria específica seja identificada, a tarefa recebe:

GERAL

⸻

Status das tarefas

Toda nova tarefa é criada inicialmente como:

PENDENTE

Quando o usuário conclui uma tarefa, seu status é alterado para:

CONCLUÍDA

⸻

Banco de dados

O projeto utiliza SQLite para armazenar as tarefas.

O banco de dados é criado automaticamente com o nome:

tarefas.db

As principais informações armazenadas são:

Campo	Descrição
ID	Identificador da tarefa
Texto original	Solicitação digitada pelo usuário
Título	Título da tarefa
Responsável	Pessoa responsável
Prazo	Data limite da tarefa
Prioridade	Prioridade da tarefa
Categoria	Categoria da tarefa
Status	Situação da tarefa
Criada em	Data e hora de criação

⸻

Importação e exportação JSON

O sistema permite exportar as tarefas cadastradas para um arquivo JSON.

Também é possível importar tarefas de um arquivo JSON para o banco de dados.

Essa funcionalidade permite salvar e transportar os dados das tarefas.

⸻

Faker

O projeto utiliza a biblioteca Faker para gerar dados fictícios.

Essa funcionalidade é utilizada para testes e permite criar automaticamente tarefas sem precisar cadastrar cada uma manualmente.

⸻

Tecnologias utilizadas

Tecnologia	Utilização
Python	Linguagem principal
Tkinter	Desenvolvimento da interface gráfica
SQLite	Armazenamento das tarefas
JSON	Importação e exportação dos dados
Regex (re)	Identificação de informações no texto
datetime	Manipulação de datas e horários
Faker	Geração de dados fictícios para testes

⸻

Instalação

É necessário ter o Python instalado.

Depois, instale a biblioteca Faker:

pip install Faker

As demais bibliotecas utilizadas no projeto fazem parte da biblioteca padrão do Python ou acompanham o Tkinter.

⸻

Como executar

Interface gráfica

Salve o código da versão Tkinter em um arquivo .py.

Por exemplo:

app.py

Execute pelo terminal:

python app.py

Interface CLI

Salve o código da versão de terminal em um arquivo .py.

Por exemplo:

cli.py

Execute:

python cli.py

⸻

Estrutura do projeto

Uma estrutura possível para os arquivos é:

Automacao-de-Tarefas/
│
├── app.py
├── cli.py
├── tarefas.db
├── tarefas.json
└── README.md

O arquivo tarefas.db é criado automaticamente durante a execução do sistema.

O arquivo tarefas.json é criado quando as tarefas são exportadas.

⸻

Exemplo de utilização

Solicitação

A Maria precisa enviar a proposta para o cliente até sexta. É urgente.

Informações identificadas

Responsável: Maria
Prazo: sexta-feira
Prioridade: ALTA
Categoria: CLIENTE / VENDAS
Status: PENDENTE

A tarefa fica armazenada no banco de dados e pode ser posteriormente consultada, concluída ou excluída.

⸻

Fluxo de utilização

1. Usuário escreve uma solicitação
              ↓
2. Sistema analisa o texto
              ↓
3. Sistema identifica responsável
              ↓
4. Sistema identifica prazo
              ↓
5. Sistema identifica prioridade
              ↓
6. Sistema identifica categoria
              ↓
7. Tarefa é criada
              ↓
8. Tarefa é armazenada no SQLite
              ↓
9. Usuário pode gerenciar a tarefa

⸻

Conceitos de programação utilizados

Durante o desenvolvimento do projeto foram utilizados conceitos como:

* Funções;
* Variáveis;
* Estruturas condicionais;
* Laços de repetição;
* Manipulação de strings;
* Expressões regulares;
* Manipulação de datas;
* Banco de dados;
* Operações CRUD;
* Arquivos JSON;
* Interface gráfica;
* Interface de terminal;
* Bibliotecas externas;
* Geração de dados para testes.

⸻

Limitações

A identificação das informações é realizada através de regras e padrões definidos no código, e não por um modelo de inteligência artificial.

Por isso, solicitações que utilizem palavras ou estruturas muito diferentes das previstas podem não ter todas as informações identificadas.

Quando uma informação não é encontrada, o sistema utiliza valores padrão, como:

Responsável: Não definido
Prazo: Não definido
Prioridade: BAIXA
Categoria: GERAL
Status: PENDENTE

⸻

📌 CONCLUÇÃO 📌

A Automação de Tarefas busca facilitar a organização e o gerenciamento de atividades através da automatização da criação de tarefas.

A partir de uma simples solicitação escrita, o sistema consegue identificar informações relevantes e armazená-las de forma estruturada, permitindo que as tarefas sejam posteriormente consultadas, organizadas e concluídas.

O projeto demonstra a aplicação prática de Python, SQLite, Tkinter, JSON, Regex e Faker em um sistema de automação e gerenciamento de tarefas.
















# projetos_cdt
About Repositório dedicado ao estudo e prática de Metodologias Ágeis. Este espaço visa compartilhar conhecimento sobre os frameworks mais populares (Scrum, Kanban, etc.), princípios de desenvolvimento ágil e ferramentas que promovem flexibilidade e eficiência. Sinta-se à vontade para explorar, aprender e contribuir!
