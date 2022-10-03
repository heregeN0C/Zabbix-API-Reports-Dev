from session import connect
import datetime
import time
from matplotlib import pyplot as plt
import zoneinfo

zbx = connect()

def main():

    hostGroup = input('Insira o Id do grupo de hosts: ')
    res = zbx.do_request(method='hostgroup.get', params={'groupids':hostGroup})
    print(f'Nome do grupo selecionado: {res["result"][0]["name"]}')

    hosts = zbx.do_request(method='host.get', params={'groupids':hostGroup})
    # print(hosts) 0SOMENTE DEBUG

    if hosts['result']!=None:
        print('\nLista de hosts existentes (Id | Nome do host):\n')
        for i in hosts['result']:
            print(f'{i["hostid"]} | {i["host"]}')
        hostId = input('\nDigite o id do host que deseja: ')
        dataInicio = input('\nDigite a data de início desejada(dd/mm/aaaa hh:mm): ')
        dataFinal = input('\nDigite a data final desejada(dd/mm/aaaa hh:mm): ')
        itemId = input('\nDigite o id do item que deseja(no momento somente itens de consumo de banda são aceitos): ')

        dataInicioTimestamp = time.mktime(datetime.datetime.strptime(dataInicio,'%d/%m/%Y %H:%M').timetuple())
        dataFinalTimestamp = time.mktime(datetime.datetime.strptime(dataFinal, '%d/%m/%Y %H:%M').timetuple())

        history_query = zbx.do_request(method='history.get', params={
            'hostids': hostId, 'time_from':int(dataInicioTimestamp),
            'time_till': int(dataFinalTimestamp),
            'itemids': itemId,
            'sortfield': 'clock'
            })

        tempo = []
        dados = []
        for y in history_query['result']:
            tempo.append(y['clock'])
            dados.append(y['value'])

        ######## CONVERTE DADOS DAS LISTAS PARA NÚMEROS INTEIROS ##########
        dadosInteiros = []
        tempoInteiro = []
        for i in dados:
            dadosInteiros.append(int(i))
        for a in tempo:
            tempoInteiro.append(int(a))
        ###################################################################

        ####### CONVERTE DADOS EM BITS POR SEGUNDO PARA MEGABITS POR SEGUNDO ########
        dadosEmMbps = []
        for b in range(len(dadosInteiros)):
            dadosEmMbps.append(dadosInteiros[b]/1000000)

        #############################################################################

        ####33# CONVERTE TEMPO DE TIMESTAMP DE VOLTA PARA DATETIME ##################
        tempoEmDatetime = []
        for c in range(len(tempoInteiro)):
            tempoEmDatetime.append(datetime.datetime.fromtimestamp(tempoInteiro[c]).strftime('%d/%m %H:%M'))
        #############################################################################
        # print(tempoEmDatetime,'\n',dadosEmMbps)

        plt.figure(figsize=(28, 18))
        plt.ylabel('tráfego em Mbps')
        plt.xlabel('tempo percorrido')
        fig, ax = plt.subplots()
        ax.plot(tempoEmDatetime, dadosEmMbps, markersize=12)
        ax.grid(True)
        ax.tick_params(axis='x' ,labelrotation=90, labelsize='medium', width=3)
        plt.show()
        # plt.savefig(fname='teste_imagem_em_pdf', format='png')
    else:
        print('erro ao selecionar grupo de host!')
main()