# SteamPy

Aplicação de linha de comando em Python para simular uma plataforma de gerenciamento de jogos digitais (nos moldes da Steam), a partir de um catálogo carregado de um arquivo CSV.

Projeto acadêmico desenvolvido em grupo para a disciplina de Programação de Computadores.

## Funcionalidades

* **Catálogo de jogos**: carregamento a partir de um arquivo CSV, armazenado em lista e indexado por ID em um dicionário para busca rápida.
* **Busca e filtros**: por nome, gênero, console, nota mínima, vendas mínimas, publisher e ano de lançamento.
* **Ordenação**: por título, nota, vendas totais, data de lançamento, console ou gênero.
* **Backlog (fila)**: permite adicionar jogos a uma fila de "para jogar depois", com persistência em `backlog.txt`.
* **Jogos recentes (pilha)**: mantém o histórico dos últimos jogos jogados ou retomados, com limite de 20 itens e persistência em `recentes.txt`.
* **Sessões de jogo**: registra o tempo jogado por sessão, calcula o status do jogo e mantém um histórico completo em `historico_jogo.txt`.
* **Recomendações**: sistema de pontuação baseado em características do histórico do usuário, como gênero, console, nota média e publisher.
* **Ranking pessoal**: apresenta informações como jogos mais jogados, gêneros e consoles mais utilizados e jogos com melhores avaliações dentro do histórico.
* **Dashboard**: painel com estatísticas gerais de utilização, incluindo tempo total jogado, média por sessão, jogo mais jogado, gênero e console favoritos, nota média e distribuição por status.
* **Menu interativo**: todas as funcionalidades são acessadas por meio de um menu no terminal.

## Tecnologias

* Python
* `csv`
* `os`
* `datetime`

O projeto utiliza apenas bibliotecas nativas do Python e não possui dependências externas.

## Conceitos aplicados

O projeto coloca em prática conceitos fundamentais de programação, incluindo:

* Programação Orientada a Objetos (POO)
* Classes e métodos
* Listas e dicionários
* Estruturas de dados de fila e pilha
* Leitura e manipulação de arquivos CSV
* Persistência de dados em arquivos TXT
* Manipulação de datas e horários
* Funções e regras de negócio
* Busca, filtragem e ordenação de dados
* Organização de funcionalidades em diferentes classes

## Estrutura principal

O projeto é organizado principalmente no arquivo:

```text
SteamPy/
├── steam.py
├── README.md
├── .gitignore
└── dataset.csv
```

O `dataset.csv` é utilizado como fonte de dados durante a execução, mas não está incluído no repositório devido à origem e às condições de utilização dos dados de terceiros.

Durante a execução, o sistema também pode criar arquivos de persistência, como:

```text
backlog.txt
recentes.txt
historico_jogo.txt
```

## Como executar

Clone o repositório e acesse a pasta do projeto.

Em seguida, execute:

```bash
python steam.py
```

O programa espera um arquivo `dataset.csv` no mesmo diretório, contendo uma estrutura de colunas compatível com:

```text
img,title,console,genre,publisher,developer,critic_score,total_sales,na_sales,jp_sales,pal_sales,other_sales,release_date,last_update
```

> O dataset utilizado durante o desenvolvimento não está incluído neste repositório, pois se trata de dados de terceiros cuja origem/licença não foi totalmente esclarecida. Para executar o sistema, utilize um CSV próprio com a mesma estrutura de colunas.

## Contexto acadêmico

O SteamPy foi desenvolvido **em grupo, com colegas**, como projeto acadêmico para a disciplina de Programação de Computadores.

Durante o desenvolvimento, foram utilizadas **ferramentas de Inteligência Artificial como copiloto**, principalmente para apoio na implementação, esclarecimento de dúvidas, investigação de soluções e revisão de código.

A utilização de IA fez parte do processo de desenvolvimento, mas o projeto também teve como objetivo aplicar e consolidar os conceitos de programação estudados na disciplina.

## Objetivo do projeto

O objetivo do SteamPy foi transformar conceitos fundamentais de programação em uma aplicação prática, simulando funcionalidades de uma plataforma de gerenciamento de jogos.

Além da manipulação de dados, o projeto permitiu trabalhar com estruturas de dados, programação orientada a objetos, persistência de informações e desenvolvimento de regras de negócio em uma aplicação interativa de terminal.
