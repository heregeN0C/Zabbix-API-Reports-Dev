import numpy as np
from session import connect
import datetime
import time
from matplotlib import pyplot as plt, artist

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
        dataInicioTimestamp = time.mktime(datetime.datetime.strptime(dataInicio,'%d/%m/%Y %H:%M').timetuple())
        dataFinalTimestamp = time.mktime(datetime.datetime.strptime(dataFinal, '%d/%m/%Y %H:%M').timetuple())

        history_query = zbx.do_request(method='history.get', params={
            'hostids': hostId, 'time_from':int(dataInicioTimestamp),
            'time_till': int(dataFinalTimestamp),
            'itemids': '1285279',
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
        # print(tempoInteiro,'\n',dadosInteiros)

        plt.figure(figsize=(12, 10))
        plt.plot(tempoInteiro, dadosInteiros)
        plt.show()

    else:
        print('erro ao selecionar grupo de host!')
main()