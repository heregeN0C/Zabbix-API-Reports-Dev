from django.shortcuts import render
from django.http import HttpResponse
from pyzabbix import ZabbixAPI
from . import forms
import re
from datetime import datetime
import matplotlib.pyplot as plt
# Create your views here.

token = "888f5efeca7d1cda0ecc2b468f284ea41e8cc28889730abd5a2f3b41fca2a586"
server = "https://lunio.cloudprovtel.com/"

zapi = ZabbixAPI(server)
zapi.login(api_token=token)

def mainPage(request):
    if not zapi.is_authenticated:
        zapi.login(api_token=token)
        version = zapi.api_version()
        #coletar grupos de hosts
        try:
            payload = {
                "output": ["groupid", "name"]
            }
            r = zapi.do_request("hostgroup.get", payload)
            group_list = r["result"]
            #print(group_list)
            return render(request, 'main.html', context={"version": version, "group_list": group_list})

        except Exception as e:
            print("Erro ao executar o metodo: ", e)


    else:
        version = zapi.api_version()
        # coletar grupos de hosts
        try:
            payload = {
                "output": ["groupid", "name"]
            }
            r = zapi.do_request("hostgroup.get", payload)
            group_list = r["result"]
            #print(group_list)
            return render(request, 'main.html', context={"version": version, "group_list": group_list})

        except Exception as e:
            print("Erro ao executar o metodo: ", e)

def hostSelect(request):
    if request.method == ('POST'):
        form = forms.GroupForm(request.POST)
        if form.is_valid():
            group_select = str(form.cleaned_data['group_select'])
            if group_select:
                pattern = r"^\d+"
                match = re.match(pattern, group_select)
                if match:
                    groupid = str(match.group())

                    #Fazer requisicao na api do zabbix
                    payload = {
                        "output": ["hostid","host"],
                        "groupids": groupid
                    }
                    r = zapi.do_request("host.get", payload)
                    host_list = r["result"]

                    #TODO: Transformar o retorno da lista em JSON, e Salvar o hostid como cookie

                    # Definir um cookie com mais opções
                    response = render(request, 'hosts.html', context={"host_list": host_list})

                    return response

            else:
                raise ValueError("O campo de selecao do grupo nao está sendo passado.")
        else:
            erros = form.errors
            # raise ValidationError("Um ou mais campos incorretos")
            return render(request, 'hosts.html', {'erros': erros})
    else:
        form = forms.HostForm()
        return render(request, 'hosts.html', context={"form": form})

def MetricsSelect(request):
    if request.method == ('POST'):
        form = forms.HostForm(request.POST)
        if form.is_valid():
            host_select = str(form.cleaned_data['host_select'])
            if host_select:
                pattern = r"^\d+"
                match = re.match(pattern, host_select)
                if match:
                    hostid = str(match.group())

                    #Fazer requisicao dos graficos disponiveis na api do zabbix
                    payload = {
                        "output": ["graphid","name"],
                        "hostids": hostid
                    }
                    r = zapi.do_request("graph.get", payload)
                    graph_list = r["result"]

                    response = render(request, 'graph.html', context={"graph_list": graph_list})
                    response.set_cookie(key='host_id', value=hostid)
                    return response

            else:
                raise ValueError("O campo de selecao do grupo nao está sendo passado.")
        else:
            erros = form.errors
            # raise ValidationError("Um ou mais campos incorretos")
            return render(request, 'graph.html', {'erros': erros})
    else:
        #form = forms.GraphForm()
        return render(request, 'graph.html')

def reportGen(request):
    if request.method == 'POST':
        form = forms.ReportForm(request.POST)
        if form.is_valid():
            graph = str(form.cleaned_data['graph_select'])
            date = str(form.cleaned_data['date_select'])
            time = str(form.cleaned_data['time_select'])
            date_end = str(form.cleaned_data['date_end_select'])
            time_end = str(form.cleaned_data['time_end_select'])
            data_inicio = date+" "+time
            data_inicio_formatada = datetime.strptime(data_inicio, '%Y-%m-%d %H:%M')
            data_final = date_end+" "+time_end
            data_final_formatada = datetime.strptime(data_final, '%Y-%m-%d %H:%M')

            pattern = r"^\d+"
            match = re.match(pattern, graph)
            if match:
                graphid = str(match.group())

                hostid = request.COOKIES['host_id']
                payload_gitem = {
                    "hostid": hostid,
                    "graphids": graphid,
                    "selectItems": ["itemid", "name"]
                }

                r_gitem = zapi.do_request("graphitem.get", payload_gitem)

                for row in r_gitem['result']:
                    itemid = row["itemid"]
                    # coletar historico do item
                    payload_history = {
                        "itemids": itemid,
                        "hostids": hostid,
                        "time_from": int(data_inicio_formatada.timestamp()),  # Certifique-se de que este tempo esteja correto
                        "time_till": int(data_final_formatada.timestamp()),
                        "sortfield": "clock",
                        "sortorder": "ASC"
                    }

                    r_history = zapi.do_request("history.get", payload_history)

                    time_ha = []
                    value_ha = []
                    for i in range(len(r_history["result"])):
                        # Converter o timestamp Unix para uma data legível
                        time_ha.append(datetime.fromtimestamp(int(r_history["result"][i]["clock"])))
                        # Converter o valor para float
                        valor_convertido = float(r_history["result"][i]["value"]) / 1000000
                        value_ha.append(round(valor_convertido, 2))

                    fig, ax = plt.subplots()
                    ax.plot(time_ha, value_ha)
                    ax.set_xlabel('Time')
                    ax.set_ylabel('Value')

                    plt.show()

                    return render(request, 'sucess.html')
            else:
                print("erro ao coletar graphid")

        else:
            erros = form.errors
            return render(request, 'graph.html', {'erros':erros})
