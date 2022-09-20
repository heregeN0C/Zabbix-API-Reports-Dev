from pyzabbix import ZabbixAPI
from session import connect

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
    else:
        print('erro ao selecionar grupo de host!')
main()