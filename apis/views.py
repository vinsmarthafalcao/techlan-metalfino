from django.http import HttpRequest, JsonResponse
from django.db.models import Q
from .models import *
from login.services.seniorBackends import require_authentication, getUserSession, getDataSession
from datetime import datetime
from app.seniorSettings import CODEMP, DEPOSITOS
from apontamento.services.packageManager import getPackage
from login.models import UserComplement
import json



@require_authentication
def listaProdutos(request: HttpRequest):
    inpText = json.loads(request.body).get('texto', '')
    filtros = json.loads(request.body).get('filtros', '')
    exclusoes = json.loads(request.body).get('exclusoes', '')
    filtros['codemp'] = CODEMP
    filtros['sitorp__in'] = ['A', 'L']
    if (inpText): filtros['codpro__icontains'] = inpText
    
    produtos = OrdensProducao.objects.filter(**filtros).exclude(**exclusoes).values('codpro', 'codori')
    return JsonResponse(list(produtos), safe=False)

@require_authentication
def listaOrigens(request: HttpRequest):
    inpText = json.loads(request.body).get('texto', '')
    filtros = json.loads(request.body).get('filtros', '')
    exclusoes = json.loads(request.body).get('exclusoes', '')
    filtros['codemp'] = CODEMP
    filtros['sitorp__in'] = ['A', 'L']
    if (inpText): filtros['codori__icontains'] = inpText
    origens = OrdensProducao.objects.filter(**filtros).exclude(**exclusoes).values('codori') 
    
    return JsonResponse(list(origens), safe=False)

@require_authentication
def listaCentroRecursos(request: HttpRequest):
    inpText = json.loads(request.body).get('texto', '')
    filtros = json.loads(request.body).get('filtros', '')
    exclusoes = json.loads(request.body).get('exclusoes', '')
    filtros['codemp'] = CODEMP
    if (inpText): filtros['codcre__icontains'] = inpText

    c_recursos = C_Recursos.objects.filter(**filtros).exclude(**exclusoes).values('codcre', 'descre', 'codetg')
    
    return JsonResponse(list(c_recursos), safe=False)

@require_authentication
def listaOps(request: HttpRequest):
    data = json.loads(request.body)
    codori, codpro = data.get('codori', ''), data.get('codpro', '')
    try: numorp = int(data.get('numorp'))
    except: numorp = ''

    filtros = Q(codemp=CODEMP, sitorp__in=["A", "L"])
    if codori: filtros &= Q(codori=codori)
    if codpro: filtros &= Q(codpro=codpro)
    if numorp: filtros &= Q(numorp=numorp)

    ops = OrdensProducao.objects.filter(filtros).values('codori', 'numorp', 'codpro', 'sitorp', 'datger')
    return JsonResponse(list(ops), safe=False)


@require_authentication
def listaOperadores(request: HttpRequest):
    inpText = json.loads(request.body).get('texto', '')
    operadoresQuery = Operadores.objects.filter(
        (Q(numcad__icontains=inpText) | Q(nomope__icontains=inpText)), codemp=CODEMP
    ).values('numcad', 'nomope') if inpText else []
    
    operadores = []
    operadores.extend({"numcad":f'{operador["numcad"]}-{operador["nomope"]}'} 
                      for operador in operadoresQuery)
    
    return JsonResponse(list(operadores), safe=False)  


@require_authentication
def listaMoldes(request: HttpRequest):
    inpText = json.loads(request.body).get('texto', '')
    filtros = json.loads(request.body).get('filtros', '')
    filtros['codemp'] = CODEMP
    filtros['sitmol'] = 'A'
    if (inpText): filtros['codmolde__icontains'] = inpText
    
    moldes = MoldePro.objects.filter(**filtros).values('codmolde', 'codpro', 'sitmol')
        
    return JsonResponse(list(moldes), safe=False)


@require_authentication
def getDataOp(request: HttpRequest):
    # Informações da OP vindas da requisição
    data = json.loads(request.body)
    codori = data.get('codori', '')
    try: numorp = int(data.get('numorp'))
    except: return JsonResponse(None, safe=False)
    # Informações complementares da OP
    try: op = ComplementoOp.objects.get(codemp = CODEMP, codori=codori, numorp=numorp)
    except: return JsonResponse(None, safe=False)
    if (op.related(OrdensProducao).sitorp not in ["A", "L"]): return JsonResponse(None, safe=False)   
    deposito = op.related(Deposito).desdep
    data_nula = datetime(1900, 12, 31)
    # Informações de roteiro da OP
    roteiros = RoteirosOP.objects.filter(
    Q(codemp = CODEMP) & Q(codori=codori) & Q(numorp=numorp) & Q(dtrfim=data_nula)
    ).values('codemp', 'codetg', 'seqrot', 'codopr', 'codcre')
    # Informações dos componentes da OP
    componentes = ComponentesOP.objects.filter(Q(codemp = CODEMP) & Q(codori=codori) & Q(numorp=numorp)
                ).values('codetg', 'seqcmp', 'codcmp', 'qtdprv')
    # Operador do usuário
    user = getUserSession(getDataSession(request))
    userComplement = UserComplement.objects.get(codemp=CODEMP, codusu=user.codusu)
    operador = None
    if (userComplement.numcad): operador = userComplement.related(Operadores)
    # montagem da resposta  
    OpData = {
        "codori": op.codori,
        "numorp":op.numorp,
        "codpro":op.codpro,
        "qtdprv":op.qtdprv,
        "coddep": op.coddep,
        "desdep":deposito,
        "datatu": datetime.now().strftime('%Y-%m-%dT%H:%M'),
        "numcad": f"{operador.numcad}-{operador.nomope}" if operador else "",
        "roteiro": [],
        "componentes": list(componentes)
    }
    # montagem do roteiro na resposta
    for roteiro in roteiros:
        desetg = Estagios.objects.get(codemp=roteiro['codemp'], codetg=roteiro['codetg']).desetg
        desopr = Operacoes.objects.get(codemp=roteiro['codemp'], codopr=roteiro['codopr']).desopr
        OpData['roteiro'].append({
            "codetg":f"{roteiro['codetg']}-{desetg}",
            "seqrot":f"{roteiro['seqrot']}-{desopr}",
            "codcre":roteiro['codcre']
        })

    
    return  JsonResponse(OpData, safe=False)


@require_authentication
def getPackageView (request: HttpRequest):
    codePackage = json.loads(request.body)
    try: 
        return JsonResponse(getPackage(codePackage), safe=False)
    except: 
        return JsonResponse(None, safe=False)


@require_authentication
def getDepositDestination(request: HttpRequest):
    deposit = json.loads(request.body)
    try: desdep = Deposito.objects.get(codemp=CODEMP, coddep=DEPOSITOS[deposit]).desdep
    except: return JsonResponse({'coddep':'', 'desdep':''}, safe=False)
    return JsonResponse({'coddep':DEPOSITOS[deposit], 'desdep':desdep}, safe=False)

  
    
    
    
    




        
    
    
    
    
     
    
    
    

 
    



