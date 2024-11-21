from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from login.services.seniorBackends import require_authentication, getDataSession, getUserSession
from .services.prodReporting import toProdReporting
from .services.packageManager import createPackages, validatePackages, printTags, reportingPackages
from app.seniorSettings import IMPRESSORAS
import json
# import win32print

@require_authentication
def noteProduction_INJ(request: HttpRequest):
    if (request.method == "GET"): return render(request, 'Apontamento_INJ.html') 
    if (request.method == "POST"): 
        prodReporting = json.loads(request.body)
        if (not prodReporting): return JsonResponse({"erro":True, "retorno":"Erro ao apontar!"}, safe=False)  
        
        session = getDataSession(request)
        user = getUserSession(session)
        if (validatePackages(prodReporting['embalagens'])): toProdReporting(prodReporting, session)
        if not prodReporting['erro']: createPackages(prodReporting, user)  
        return JsonResponse(prodReporting, safe=False)
    
    
@require_authentication
def noteProduction_GERAL(request: HttpRequest):
    if (request.method == "GET"): return render(request, 'Apontamento_GERAL.html') 
    if (request.method == "POST"): 
        prodReporting = json.loads(request.body)
        if (not prodReporting): return JsonResponse({"erro":True, "retorno":"Erro ao apontar!"}, safe=False)  
        
        session = getDataSession(request)
        user = getUserSession(session)
        if (validatePackages(prodReporting['embalagens'])):  toProdReporting(prodReporting, session)
        if not prodReporting['erro']: reportingPackages(prodReporting,  user)
        return JsonResponse(prodReporting, safe=False)
    
            
@require_authentication
def printTagsPackages(request: HttpRequest):
    body = json.loads(request.body)
    # Valida impressora
    estagio = body.get('estagio')
    if estagio in IMPRESSORAS: printer = IMPRESSORAS[estagio]
    else:
        body.update({'error':True, 'message':'Não existe impressora definida para esse estágio!'})
        return JsonResponse(body, safe=False)
    
    # printers = list(map(lambda printer: printer[2] ,win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)))
    # if (printer not in printers): 
    #     return JsonResponse({'error':True, 'message': "Impressora indisponível na rede do servidor!"}, safe=False);
    # Impressão
    listPackagesKeys = body.get('chavesEmbalagem')
    if (not listPackagesKeys or len(listPackagesKeys) == 0): return JsonResponse(None, safe=False)
    session = getDataSession(request)
    response = printTags(listPackagesKeys, session, printer)
    body.update(response)
    return JsonResponse(body, safe=False)



    
          

