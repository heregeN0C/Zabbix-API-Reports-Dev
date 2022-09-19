from bokeh.plotting import figure, show
import requests
from datetime import datetime


url = 'http://mob.cloudprovtel.com/api_jsonrpc.php'
token = '55a634b9b4ad9256afe7a8081a4a26283418acb3a9301b18699beeb9df52efb6'

def filtroReport():

    payload = {
        "jsonrpc": "2.0",
        "method": "history.get",
        "params": {
            "output": "extend",
            "hostids": "10667",
            "itemids": "142368",
            "sortfield": "clock",
            "limit": 10,
        },
        "auth": token,
        "id": 1,
    }

    r = requests.post(url=url, json=payload)

    return r.json()

res = filtroReport()
#print(res)

valores = []
tempo = []
for y in range(len(res['result'])):
    valores.append(res['result'][y]['value'])
    tempo.append(res['result'][y]['clock'])


p = figure(title="teste", x_axis_label='data/hora', y_axis_label='valor')

p.line(tempo, valores, line_width=1)
show(p)
#print(valores)