# SteamPy
Aplicação em Python para leitura, consulta e manipulação de dados de jogos da Steam a partir de arquivos CSV.

# SteamPy

Aplicação de linha de comando em Python para simular uma plataforma de gerenciamento de jogos digitais (nos moldes da Steam), a partir de um catálogo carregado de um arquivo CSV. Projeto acadêmico desenvolvido para a disciplina de Programação de Computadores.

## Funcionalidades

- **Catálogo de jogos**: carregamento a partir de um arquivo CSV, armazenado em lista e indexado por ID em um dicionário para busca rápida.
- **Busca e filtros**: por nome, gênero, console, nota mínima, vendas mínimas, publisher e ano de lançamento.
- **Ordenação**: por título, nota, vendas totais, data de lançamento, console ou gênero.
- **Backlog (fila)**: adicionar jogos a uma fila de "para jogar depois", com persistência em `backlog.txt`.
- **Jogos recentes (pilha)**: histórico dos últimos jogos jogados/retomados, com limite de 20 itens e persistência em `recentes.txt`.
- **Sessões de jogo**: registro de tempo jogado por sessão, com cálculo automático de status (`iniciado`, `em andamento`, `muito jogado`, `concluído simbolicamente`) e histórico completo salvo em `historico_jogo.txt`.
- **Recomendações**: sistema de pontuação que combina gênero favorito, console favorito, nota média jogada e publisher recorrente, evitando sugerir jogos já muito jogados ou já presentes no backlog.
- **Ranking pessoal**: jogos mais jogados por tempo, gêneros e consoles mais jogados, e top jogos por nota dentro do histórico do usuário.
- **Dashboard**: painel com estatísticas gerais de uso (tempo total jogado, média por sessão, jogo mais jogado, gênero/console favorito, nota média, distribuição por status, etc.).
- **Menu interativo** no terminal com todas as opções acima.

## Tecnologias

Python puro — apenas bibliotecas nativas (`csv`, `os`, `datetime`), sem dependências externas.

## Como executar

```bash
python steam.py
```

O programa espera um arquivo `dataset.csv` no mesmo diretório, com as colunas:

```
img,title,console,genre,publisher,developer,critic_score,total_sales,na_sales,jp_sales,pal_sales,other_sales,release_date,last_update
```

> O dataset usado no desenvolvimento não está incluído neste repositório (dados de terceiros com origem/licença não totalmente esclarecidas). Para testar o sistema, utilize um CSV próprio com essa mesma estrutura de colunas.

Ao ser executado pela primeira vez, os arquivos `backlog.txt`, `historico_jogo.txt` e `recentes.txt` são criados automaticamente conforme o uso; se já existirem, são recarregados ao iniciar o programa.

## Contexto acadêmico

Projeto desenvolvido individualmente para a disciplina de Programação de Computadores, com apoio de ferramentas de IA para tirar dúvidas e revisar soluções durante o desenvolvimento.
