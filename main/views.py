from django.shortcuts import render
from django.http import HttpResponse
from pyzabbix import ZabbixAPI
from . import forms
import re

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
                    return render(request,'hosts.html', context={"host_list": host_list})

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
                    return render(request,'graph.html', context={"graph_list": graph_list})

            else:
                raise ValueError("O campo de selecao do grupo nao está sendo passado.")
        else:
            erros = form.errors
            # raise ValidationError("Um ou mais campos incorretos")
            return render(request, 'graph.html', {'erros': erros})
    else:
        #form = forms.GraphForm()
        return render(request, 'graph.html')