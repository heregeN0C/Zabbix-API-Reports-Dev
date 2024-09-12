from django.shortcuts import render
from django.http import HttpResponse
from pyzabbix import ZabbixAPI


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

