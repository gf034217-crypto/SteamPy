import csv
import os
from datetime import datetime


class Jogo:
    def __init__(self, id_jogo, titulo, console, genero, publisher, developer, critic_score, total_vendas, vendas_an, vendas_jp, vendas_eu, outras_vendas, data_lanc):
        self.id_jogo = id_jogo
        self.titulo = titulo
        self.console = console
        self.genero = genero
        self.publisher = publisher
        self.developer = developer
        self.critic_score = critic_score
        self.total_vendas = total_vendas
        self.vendas_an = vendas_an
        self.vendas_jp = vendas_jp
        self.vendas_eu = vendas_eu
        self.outras_vendas = outras_vendas
        self.data_lanc = data_lanc

    def exibir(self):
        print(f'{self.id_jogo} , {self.titulo} , {self.console} , {self.genero} , {self.publisher} , {self.developer} , {self.critic_score} , {self.total_vendas} , {self.vendas_an} , {self.vendas_jp} , {self.vendas_eu} , {self.outras_vendas} , {self.data_lanc}')

    def linha_backlog(self):
        return f'{self.id_jogo};{self.titulo};{self.console}'

    def linha_recentes(self):
        return f'{self.id_jogo};{self.titulo};{self.console}'


class FilaBacklog:
    def __init__(self):
        self.dados = []

    def enqueue(self, jogo):
        self.dados.append(jogo)

    def dequeue(self):
        if self.is_empty():
            return None
        return self.dados.pop(0)

    def is_empty(self):
        return len(self.dados) == 0

    def mostrar(self):
        if self.is_empty():
            print('Backlog vazio')
            return
        for i, jogo in enumerate(self.dados, start=1):
            print(f'[{i}] {jogo.titulo} | {jogo.console}')

    def tamanho(self):
        return len(self.dados)

    def contem(self, id):
        for jogo in self.dados:
            if jogo.id_jogo == id:
                return True
        return False


class PilhaRecentes:
    def __init__(self, limite=20):
        self.dados = []
        self.limite = limite

    def push(self, jogo):
        indice = -1
        for i in range(len(self.dados)):
            if self.dados[i].id_jogo == jogo.id_jogo:
                indice = i
                break
        if indice != -1:
            self.dados.pop(indice)
        self.dados.append(jogo)
        if len(self.dados) > self.limite:
            self.dados.pop(0)

    def pop(self):
        if self.is_empty():
            return None
        return self.dados.pop()

    def topo(self):
        if self.is_empty():
            return None
        return self.dados[-1]

    def is_empty(self):
        return len(self.dados) == 0

    def tamanho(self):
        return len(self.dados)

    def mostrar(self):
        if self.is_empty():
            print('Nenhum jogo recente')
            return
        for i in range(len(self.dados) - 1, -1, -1):
            print(f'{self.dados[i].titulo} | {self.dados[i].console}')


class SessaoJogo:
    def __init__(self, jogo, tempo_jogado, tempo_total, status):
        self.jogo = jogo
        self.tempo_jogado = tempo_jogado
        self.tempo_total = tempo_total
        self.data_sessao = datetime.now().strftime('%d/%m/%Y %H:%M')
        self.status = status
        self.percentual_simulado = min((tempo_total / 20) * 100, 100)

    def exibir(self):
        print(f'{self.jogo.titulo} | Sessao: {self.tempo_jogado}h | Total: {self.tempo_total}h | Status: {self.status} | Data: {self.data_sessao}')

    def linha_historico(self):
        return f'{self.jogo.titulo};{self.tempo_jogado};{self.tempo_total};{self.status};{self.data_sessao}'
        

class SteamPy:
    def __init__(self):
        self.catalogo = []
        self.indice_jogos = {}
        self.backlog = FilaBacklog()
        self.recentes = PilhaRecentes(limite=20)
        self.historico = []
        self.tempo_por_jogo = {}

    def carregar_jogos(self, nome_arquivo):
        self.catalogo = []
        self.indice_jogos = {}
        try:
            with open(nome_arquivo, encoding='utf-8') as f:
                leitor = csv.reader(f)
                next(leitor)
                id_contador = 1
                for linha in leitor:
                    try:
                        if len(linha) < 13:
                            continue
                        titulo = linha[1]
                        console = linha[2]
                        genero = linha[3]
                        publisher = linha[4]
                        developer = linha[5]
                        critic_score = float(linha[6]) if linha[6] else 0.0
                        total_vendas = float(linha[7]) if linha[7] else 0.0
                        na_sales = float(linha[8]) if linha[8] else 0.0
                        jp_sales = float(linha[9]) if linha[9] else 0.0
                        pal_sales = float(linha[10]) if linha[10] else 0.0
                        other_sales = float(linha[11]) if linha[11] else 0.0
                        release_date = linha[12]
                        last_update = linha[13] if len(linha) > 13 else ''
                        jogo = Jogo(id_contador, titulo, console, genero, publisher, developer,
                                    critic_score, total_vendas, na_sales, jp_sales, pal_sales,
                                    other_sales, release_date)
                        self.catalogo.append(jogo)
                        self.indice_jogos[id_contador] = jogo
                        id_contador += 1
                    except Exception:
                        continue
            print(f'{len(self.catalogo)} jogos carregados com sucesso.')
        except FileNotFoundError:
            print(f'Arquivo {nome_arquivo} nao encontrado.')

    def listar_jogos(self):
        if not self.catalogo:
            print('Catalogo vazio.')
            return
        for jogo in self.catalogo:
            print(f'[{jogo.id_jogo}] {jogo.titulo} | {jogo.console} | {jogo.genero} | Nota: {jogo.critic_score}')

    def buscar_jogo_por_nome(self, termo):
        resultados = [j for j in self.catalogo if termo.lower() in j.titulo.lower()]
        if not resultados:
            print('Nenhum jogo encontrado.')
            return []
        for jogo in resultados:
            print(f'[{jogo.id_jogo}] {jogo.titulo} | {jogo.console} | Nota: {jogo.critic_score}')
        return resultados

    def filtrar_por_genero(self, genero):
        resultados = [j for j in self.catalogo if j.genero.lower() == genero.lower()]
        if not resultados:
            print('Nenhum jogo encontrado para esse genero.')
            return []
        for jogo in resultados:
            print(f'[{jogo.id_jogo}] {jogo.titulo} | {jogo.console} | Nota: {jogo.critic_score}')
        return resultados

    def filtrar_por_console(self, console):
        resultados = [j for j in self.catalogo if j.console.lower() == console.lower()]
        if not resultados:
            print('Nenhum jogo encontrado para esse console.')
            return []
        for jogo in resultados:
            print(f'[{jogo.id_jogo}] {jogo.titulo} | {jogo.console} | Nota: {jogo.critic_score}')
        return resultados

    def filtrar_por_nota(self, nota_minima):
        resultados = [j for j in self.catalogo if j.critic_score >= nota_minima]
        if not resultados:
            print('Nenhum jogo encontrado com essa nota minima.')
            return []
        for jogo in resultados:
            print(f'[{jogo.id_jogo}] {jogo.titulo} | Nota: {jogo.critic_score}')
        return resultados

    def filtrar_por_vendas(self, vendas_minimas):
        resultados = [j for j in self.catalogo if j.total_vendas >= vendas_minimas]
        if not resultados:
            print('Nenhum jogo encontrado com esse minimo de vendas.')
            return []
        for jogo in resultados:
            print(f'[{jogo.id_jogo}] {jogo.titulo} | Vendas: {jogo.total_vendas}')
        return resultados

    def filtrar_por_publisher(self, publisher):
        resultados = [j for j in self.catalogo if publisher.lower() in j.publisher.lower()]
        if not resultados:
            print('Nenhum jogo encontrado para essa publisher.')
            return []
        for jogo in resultados:
            print(f'[{jogo.id_jogo}] {jogo.titulo} | {jogo.publisher}')
        return resultados
    
    def filtrar_por_ano(self,ano):
        resultados = [j for j in self.catalogo if ano in j.data_lanc]
        if not resultados:
            print('Nenhum jogo encontrado para esse ano.')
            return[]
        for jogo in resultados:
            print(f'[{jogo.id_jogo}] {jogo.titulo} | {jogo.data_lanc}')
        return resultados    

    def ordenar_jogos(self, criterio):
        opcoes = {
            '1': ('titulo', False),
            '2': ('critic_score', True),
            '3': ('total_vendas', True),
            '4': ('data_lanc', False),
            '5': ('console', False),
            '6': ('genero', False),
        }
        if criterio not in opcoes:
            print('Criterio invalido.')
            return
        campo, reverso = opcoes[criterio]
        ordenados = sorted(self.catalogo, key=lambda j: getattr(j, campo) if getattr(j, campo) else '', reverse=reverso)
        for jogo in ordenados:
            print(f'[{jogo.id_jogo}] {jogo.titulo} | {jogo.console} | Nota: {jogo.critic_score} | Vendas: {jogo.total_vendas}')

    def adicionar_ao_backlog(self, id_jogo):
        if id_jogo not in self.indice_jogos:
            print('Jogo nao encontrado no catalogo.')
            return
        if self.backlog.contem(id_jogo):
            print('Esse jogo ja esta no backlog.')
            return
        jogo = self.indice_jogos[id_jogo]
        self.backlog.enqueue(jogo)
        print(f'{jogo.titulo} adicionado ao backlog.')
        self.salvar_backlog()

    def mostrar_backlog(self):
        print('=== BACKLOG ===')
        self.backlog.mostrar()

    def jogar_proximo(self):
        jogo = self.backlog.dequeue()
        if jogo is None:
            print('Backlog vazio.')
            return
        print(f'Iniciando: {jogo.titulo} | {jogo.console}')
        self._registrar_sessao_interativa(jogo)
        self.salvar_backlog()
        self.salvar_recentes()

    def salvar_backlog(self):
        with open('backlog.txt', 'w', encoding='utf-8') as f:
            f.write('id;titulo;console\n')
            for jogo in self.backlog.dados:
                f.write(jogo.linha_backlog() + '\n')

    def carregar_backlog(self):
        if not os.path.exists('backlog.txt'):
            return
        with open('backlog.txt', encoding='utf-8') as f:
            linhas = f.readlines()
        for linha in linhas[1:]:
            linha = linha.strip()
            if not linha:
                continue
            partes = linha.split(';')
            try:
                id_jogo = int(partes[0])
                if id_jogo in self.indice_jogos:
                    self.backlog.enqueue(self.indice_jogos[id_jogo])
            except Exception:
                continue
        print('Backlog carregado.')

    def _definir_status(self, total_horas):
        if total_horas < 2:
            return 'iniciado'
        elif total_horas < 10:
            return 'em andamento'
        elif total_horas < 20:
            return 'muito jogado'
        else:
            return 'concluido simbolicamente'

    def _registrar_sessao_interativa(self, jogo):
        try:
            horas = float(input(f'Quantas horas voce jogou {jogo.titulo} nessa sessao? '))
        except ValueError:
            print('Valor invalido, sessao registrada como 0h.')
            horas = 0.0
        self.registrar_sessao(jogo, horas)

    def registrar_sessao(self, jogo, tempo):
        id_jogo = jogo.id_jogo
        self.tempo_por_jogo[id_jogo] = self.tempo_por_jogo.get(id_jogo, 0.0) + tempo
        total = self.tempo_por_jogo[id_jogo]
        status = self._definir_status(total)
        sessao = SessaoJogo(jogo, tempo, total, status)
        self.historico.append(sessao)
        self.recentes.push(jogo)
        self.salvar_historico()
        self.salvar_recentes()
        print(f'Sessao registrada! Total em {jogo.titulo}: {total}h | Status: {status}')

    def mostrar_recentes(self):
        print('=== JOGOS RECENTES ===')
        self.recentes.mostrar()

    def retomar_ultimo_jogo(self):
        jogo = self.recentes.topo()
        if jogo is None:
            print('Nenhum jogo recente.')
            return
        print(f'Retomando: {jogo.titulo} | {jogo.console}')
        self._registrar_sessao_interativa(jogo)

    def salvar_historico(self):
        with open('historico_jogo.txt', 'w', encoding='utf-8') as f:
            f.write('titulo;tempo_sessao;tempo_total;status;data\n')
            for sessao in self.historico:
                f.write(sessao.linha_historico() + '\n')

    def carregar_historico(self):
        if not os.path.exists('historico_jogo.txt'):
            return
        with open('historico_jogo.txt', encoding='utf-8') as f:
            linhas = f.readlines()
        for linha in linhas[1:]:
            linha = linha.strip()
            if not linha:
                continue
            partes = linha.split(';')
            if len(partes) < 4:
                continue
            titulo = partes[0]
            try:
                tempo_sessao = float(partes[1])
                tempo_total = float(partes[2])
            except Exception:
                continue
            status = partes[3]
            jogo_encontrado = None
            for j in self.catalogo:
                if j.titulo == titulo:
                    jogo_encontrado = j
                    break
            if jogo_encontrado:
                self.tempo_por_jogo[jogo_encontrado.id_jogo] = tempo_total
                sessao = SessaoJogo(jogo_encontrado, tempo_sessao, tempo_total, status)
                self.historico.append(sessao)

    def salvar_recentes(self):
        with open('recentes.txt', 'w', encoding='utf-8') as f:
            f.write('id;titulo;console\n')
            for jogo in self.recentes.dados:
                f.write(jogo.linha_recentes() + '\n')

    def carregar_recentes(self):
        if not os.path.exists('recentes.txt'):
            return
        with open('recentes.txt', encoding='utf-8') as f:
            linhas = f.readlines()
        for linha in linhas[1:]:
            linha = linha.strip()
            if not linha:
                continue
            partes = linha.split(';')
            try:
                id_jogo = int(partes[0])
                if id_jogo in self.indice_jogos:
                    self.recentes.push(self.indice_jogos[id_jogo])
            except Exception:
                continue

    def recomendar_jogos(self):
        if not self.historico:
            print('Jogue alguns jogos primeiro para receber recomendacoes.')
            return []

        contagem_genero = {}
        contagem_console = {}
        notas_jogadas = []
        publishers_jogados = {}
        ids_muito_jogados = set(id for id, h in self.tempo_por_jogo.items() if h >= 10)
        ids_backlog = set(j.id_jogo for j in self.backlog.dados)

        for sessao in self.historico:
            g = sessao.jogo.genero
            c = sessao.jogo.console
            p = sessao.jogo.publisher
            contagem_genero[g] = contagem_genero.get(g, 0) + 1
            contagem_console[c] = contagem_console.get(c, 0) + 1
            publishers_jogados[p] = publishers_jogados.get(p, 0) + 1
            if sessao.jogo.critic_score > 0:
                notas_jogadas.append(sessao.jogo.critic_score)

        genero_fav = max(contagem_genero, key=contagem_genero.get) if contagem_genero else None
        console_fav = max(contagem_console, key=contagem_console.get) if contagem_console else None
        nota_media = sum(notas_jogadas) / len(notas_jogadas) if notas_jogadas else 0
        publisher_fav = max(publishers_jogados, key=publishers_jogados.get) if publishers_jogados else None

        print(f'\nCriterios usados:')
        print(f'  Genero favorito      : {genero_fav}')
        print(f'  Console favorito     : {console_fav}')
        print(f'  Nota media jogada    : {nota_media:.1f}')
        print(f'  Publisher recorrente : {publisher_fav}')

        recomendados = []
        for jogo in self.catalogo:
            if jogo.id_jogo in ids_muito_jogados:
                continue
            if jogo.id_jogo in ids_backlog:
                continue
            pontos = 0
            if jogo.genero == genero_fav:
                pontos += 3
            if jogo.console == console_fav:
                pontos += 2
            if jogo.critic_score >= nota_media:
                pontos += 2
            if jogo.publisher == publisher_fav:
                pontos += 1
            if jogo.total_vendas >= 1:
                pontos += 1
            if pontos >= 3:
                recomendados.append((pontos, jogo))

        recomendados.sort(key=lambda x: x[0], reverse=True)
        recomendados = recomendados[:10]

        if not recomendados:
            print('Nenhuma recomendacao disponivel no momento.')
            return []

        print('\n=== JOGOS RECOMENDADOS PARA VOCE ===')
        for pontos, jogo in recomendados:
            print(f'[{jogo.id_jogo}] {jogo.titulo} | {jogo.console} | {jogo.genero} | Nota: {jogo.critic_score}')

        return [j for _, j in recomendados]

    def gerar_ranking_pessoal(self):
        if not self.tempo_por_jogo:
            print('Voce ainda nao jogou nenhum jogo.')
            return

        print('\n=== RANKING PESSOAL ===')

        print('\n-- Jogos mais jogados (por tempo) --')
        jogos_tempo = sorted(self.tempo_por_jogo.items(), key=lambda x: x[1], reverse=True)
        for i, (id_jogo, horas) in enumerate(jogos_tempo[:10], 1):
            jogo = self.indice_jogos.get(id_jogo)
            if jogo:
                print(f'{i}. {jogo.titulo} | {horas}h | Status: {self._definir_status(horas)}')

        contagem_genero = {}
        contagem_console = {}
        for id_jogo, horas in self.tempo_por_jogo.items():
            jogo = self.indice_jogos.get(id_jogo)
            if jogo:
                contagem_genero[jogo.genero] = contagem_genero.get(jogo.genero, 0) + horas
                contagem_console[jogo.console] = contagem_console.get(jogo.console, 0) + horas

        print('\n-- Generos mais jogados --')
        for i, (genero, horas) in enumerate(sorted(contagem_genero.items(), key=lambda x: x[1], reverse=True)[:5], 1):
            print(f'{i}. {genero} | {horas:.1f}h')

        print('\n-- Consoles mais jogados --')
        for i, (console, horas) in enumerate(sorted(contagem_console.items(), key=lambda x: x[1], reverse=True)[:5], 1):
            print(f'{i}. {console} | {horas:.1f}h')

        print('\n-- Top jogos por nota (dentro do historico) --')
        jogos_historico = [self.indice_jogos[id] for id in self.tempo_por_jogo if id in self.indice_jogos]
        jogos_historico.sort(key=lambda j: j.critic_score, reverse=True)
        for i, jogo in enumerate(jogos_historico[:5], 1):
            print(f'{i}. {jogo.titulo} | Nota: {jogo.critic_score}')

    def exibir_dashboard(self):
        tempo_total = sum(self.tempo_por_jogo.values())
        total_sessoes = len(self.historico)

        jogo_mais_jogado = None
        max_horas = 0
        jogo_mais_popular = None
        max_vendas = 0
        jogo_melhor_nota = None
        max_nota = 0

        contagem_genero = {}
        contagem_console = {}
        notas_jogadas = []
        status_count = {}

        for id_jogo, horas in self.tempo_por_jogo.items():
            jogo = self.indice_jogos.get(id_jogo)
            if not jogo:
                continue
            if horas > max_horas:
                max_horas = horas
                jogo_mais_jogado = jogo
            if jogo.total_vendas > max_vendas:
                max_vendas = jogo.total_vendas
                jogo_mais_popular = jogo
            if jogo.critic_score > max_nota:
                max_nota = jogo.critic_score
                jogo_melhor_nota = jogo
            contagem_genero[jogo.genero] = contagem_genero.get(jogo.genero, 0) + horas
            contagem_console[jogo.console] = contagem_console.get(jogo.console, 0) + horas
            if jogo.critic_score > 0:
                notas_jogadas.append(jogo.critic_score)
            s = self._definir_status(horas)
            status_count[s] = status_count.get(s, 0) + 1

        genero_fav = max(contagem_genero, key=contagem_genero.get) if contagem_genero else '-'
        console_fav = max(contagem_console, key=contagem_console.get) if contagem_console else '-'
        nota_media = sum(notas_jogadas) / len(notas_jogadas) if notas_jogadas else 0
        media_por_sessao = tempo_total / total_sessoes if total_sessoes > 0 else 0
        recomendacoes = self.recomendar_jogos() if self.historico else []

        print('\n' + '=' * 50)
        print('           STEAMPY DASHBOARD')
        print('=' * 50)
        print(f'Total de jogos no catalogo    : {len(self.catalogo)}')
        print(f'Total de jogos no backlog     : {self.backlog.tamanho()}')
        print(f'Total de jogos recentes       : {self.recentes.tamanho()}')
        print(f'Total de sessoes jogadas      : {total_sessoes}')
        print(f'Tempo total jogado            : {tempo_total:.1f}h')
        print(f'Media de horas por sessao     : {media_por_sessao:.1f}h')
        print(f'Jogo mais jogado              : {jogo_mais_jogado.titulo if jogo_mais_jogado else "-"} ({max_horas:.1f}h)')
        print(f'Genero favorito               : {genero_fav}')
        print(f'Console favorito              : {console_fav}')
        print(f'Nota media dos jogos jogados  : {nota_media:.1f}')
        print(f'Jogos iniciados               : {status_count.get("iniciado", 0)}')
        print(f'Jogos em andamento            : {status_count.get("em andamento", 0)}')
        print(f'Jogos concluidos simbolic.    : {status_count.get("concluido simbolicamente", 0)}')
        print(f'Recomendacoes disponiveis     : {len(recomendacoes)}')
        print(f'Jogo mais popular ja jogado   : {jogo_mais_popular.titulo if jogo_mais_popular else "-"}')
        print(f'Jogo com melhor nota jogado   : {jogo_melhor_nota.titulo if jogo_melhor_nota else "-"}')
        print('=' * 50)

    def mostrar_historico(self):
        if not self.historico:
            print('Historico vazio.')
            return
        print('=== HISTORICO COMPLETO ===')
        for sessao in self.historico:
            sessao.exibir()


def menu():
    sistema = SteamPy()

    print('\nCarregando catalogo...')
    sistema.carregar_jogos('dataset.csv')
    sistema.carregar_backlog()
    sistema.carregar_historico()
    sistema.carregar_recentes()

    while True:
        print('\n' + '=' * 40)
        print('         STEAMPY - MENU PRINCIPAL')
        print('=' * 40)
        print('1.  Listar jogos')
        print('2.  Buscar jogo por nome')
        print('3.  Filtrar por genero')
        print('4.  Filtrar por console')
        print('5.  Filtrar por nota minima')
        print('6.  Filtrar por vendas minimas')
        print('7.  Filtrar por publisher')
        print('8.  Ordenar catalogo')
        print('9.  Adicionar jogo ao backlog')
        print('10. Ver backlog')
        print('11. Jogar proximo do backlog')
        print('12. Ver jogos recentes')
        print('13. Retomar ultimo jogo')
        print('14. Registrar tempo de jogo')
        print('15. Ver historico completo')
        print('16. Ver recomendacoes')
        print('17. Ver ranking pessoal')
        print('18. Ver dashboard')
        print('19. Salvar backlog')
        print('20. Filtrar por ano')
        print('0.  Sair')
        print('=' * 40)

        opcao = input('Escolha uma opcao: ').strip()

        if opcao == '1':
            sistema.listar_jogos()

        elif opcao == '2':
            termo = input('Digite parte do nome do jogo: ')
            sistema.buscar_jogo_por_nome(termo)

        elif opcao == '3':
            genero = input('Digite o genero: ')
            sistema.filtrar_por_genero(genero)

        elif opcao == '4':
            console = input('Digite o console: ')
            sistema.filtrar_por_console(console)

        elif opcao == '5':
            try:
                nota = float(input('Digite a nota minima: '))
                sistema.filtrar_por_nota(nota)
            except ValueError:
                print('Valor invalido.')

        elif opcao == '6':
            try:
                vendas = float(input('Digite o minimo de vendas (em milhoes): '))
                sistema.filtrar_por_vendas(vendas)
            except ValueError:
                print('Valor invalido.')

        elif opcao == '7':
            publisher = input('Digite o nome da publisher: ')
            sistema.filtrar_por_publisher(publisher)

        elif opcao == '8':
            print('Ordenar por:')
            print('1. Titulo  2. Nota  3. Vendas  4. Data  5. Console  6. Genero')
            criterio = input('Escolha: ').strip()
            sistema.ordenar_jogos(criterio)

        elif opcao == '9':
            try:
                id_jogo = int(input('Digite o ID do jogo: '))
                sistema.adicionar_ao_backlog(id_jogo)
            except ValueError:
                print('ID invalido.')

        elif opcao == '10':
            sistema.mostrar_backlog()

        elif opcao == '11':
            sistema.jogar_proximo()

        elif opcao == '12':
            sistema.mostrar_recentes()

        elif opcao == '13':
            sistema.retomar_ultimo_jogo()

        elif opcao == '14':
            try:
                id_jogo = int(input('Digite o ID do jogo: '))
                if id_jogo in sistema.indice_jogos:
                    jogo = sistema.indice_jogos[id_jogo]
                    horas = float(input(f'Quantas horas voce jogou {jogo.titulo}? '))
                    sistema.registrar_sessao(jogo, horas)
                else:
                    print('Jogo nao encontrado.')
            except ValueError:
                print('Valor invalido.')

        elif opcao == '15':
            sistema.mostrar_historico()

        elif opcao == '16':
            sistema.recomendar_jogos()

        elif opcao == '17':
            sistema.gerar_ranking_pessoal()

        elif opcao == '18':
            sistema.exibir_dashboard()

        elif opcao == '19':
            sistema.salvar_backlog()
            print('Backlog salvo.')

        elif opcao == '20':
            ano = input('Digite o ano (ex: 2015): ')
            sistema.filtrar_por_ano(ano)

        elif opcao == '0':
            sistema.salvar_backlog()
            sistema.salvar_historico()
            sistema.salvar_recentes()
            print('Ate logo!')
            break

        else:
            print('Opcao invalida.')


menu()