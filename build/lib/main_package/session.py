from pyzabbix import ZabbixAPI

def connect():
    url = 'https://lunio.cloudprovtel.com'
    username = 'api_zbx'
    password = 'Pr0vt3l*'

    zbx = ZabbixAPI(url)
    zbx.login(username,password)

    # print(f'conectado com sucesso!\nversão da api: {zbx.api_version()}')
    return zbx

# connect()