
import matplotlib.pyplot as plt
import requests

url = 'https://lunio.cloudprovtel.com/api_jsonrpc.php'
token = 'eff5bc90efacc75bd31505b5a724b0bb'

def filtroReport():

    payload = {
        "jsonrpc": "2.0",
        "method": "history.get",
        "params": {
            "output": "extend",
            "hostids": "10295",
            "itemids": "49470",
            "sortfield": "clock",
            "limit": 10,
        },
        "auth": token,
        "id": 1,
    }

    r = requests.post(url=url, json=payload)

    return r.json()

res = filtroReport()
valores = []
for y in range(len(res['result'])):
    valores.append(res['result'][y]['value'])
#print(valores)

for i in range(len(valores)):
    plt.plot(valores)
plt.show()