from django.shortcuts import render
import re
from django.http import HttpResponse,HttpResponseRedirect
from proxy_checker import ProxyChecker
import json
checker = ProxyChecker()
reg = re.compile("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\:\d{2,7}")

def red_to_index(request):
    return HttpResponseRedirect("/")
    
def match_reg(proxy):
    if reg.match(proxy):
        return True
    else:
        return False

def check_p(proxy):
    if match_reg(proxy):
        try:
            resp = checker.check_proxy(proxy)
        except:
            return "Unknown Error"
        else:
            if resp:
                return resp
            else:
                return False
    else:
        return "Syntax Error!"
        
def check_proxy(request):
    if request.method == "GET":
        prox = request.GET.get("q",None)
        if prox:
            if bool(prox):
                resp = check_p(prox)
                if type(resp) == type({'Nice':'Nice'}):
                    return HttpResponse(json.dumps(resp,indent=4))
                elif resp == "Unknown Error":
                    return HttpResponse(json.dumps({"Error":"Unknown"}))
                elif resp == "Syntax Error!":
                    return HttpResponse(json.dumps({"Error":"Invalid Syntax"}))
                else:
                     return HttpResponse(json.dumps({"Working":"False"}))
            else:
                return json.dumps({"query":"Invalid!"})
        else:
            return HttpResponseRedirect("/")