import json
from django.shortcuts import render
from login.services.seniorBackends import require_authentication, getDataSession, getUserSession
from django.http import JsonResponse
from apontamento.services.packageManager import packageTransfer


@require_authentication
def receipt_view(request):
    if request.method == 'GET':
        return render(request, 'Recebimento.html')
    elif request.method == 'POST':
        data = json.loads(request.body)
        origin = data.get('origem')
        destination = data.get('destino')
        transferList = data.get('embalagens')
        
        session = getDataSession(request)
        user = getUserSession(session)  
        response = packageTransfer(transferList, origin, destination, session, user)      
        return JsonResponse(response, safe=False)
        


