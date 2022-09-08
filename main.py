import json

import matplotlib.pyplot as plt
import requests

url = 'https://lunio.cloudprovtel.com/api_jsonrpc.php'
token = 'eff5bc90efacc75bd31505b5a724b0bb'

def filtroReport():

    payload = {
        "jsonrpc": "2.0",
        "method": "history.get",
        "params": {
            "hostids": "10295",
            "itemids": "49470",
            "time_from": 1662001200,
            "time_till": 1662605940,
        },
        "auth": token,
        "id": 1,
    }

    r = requests.post(url=url, json=payload)

    return r.json()

res = filtroReport()

# print(res)

for i in res['result']:
    for j in res['result']:
        plt.plot([j['clock']])
    plt.plot(i['value'])
plt.show()
# EXEMPLO:
# for i in stanley['items']:
#     if i['province'] == 'California':
#         print(i)