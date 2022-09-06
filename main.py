import json

import matplotlib.pyplot as plt
import requests

url = 'https://lunio.cloudprovtel.com/api_jsonrpc.php'
token = 'eff5bc90efacc75bd31505b5a724b0bb'

def filtroReport():

    payload = {
        "jsonrpc": "2.0",
        "method": "graph.get",
        "params": {
            "hostids": "10681"
        },
        "auth": token,
        "id": 1,
    }

    r = requests.post(url=url, json=payload)

    return r

resposta = filtroReport().json()
resposta = json.dumps(resposta)
# print(resposta)

width = resposta["result":0]
print(width)

# plt.plot([])
# plt.ylabel('some numbers')
# plt.show()