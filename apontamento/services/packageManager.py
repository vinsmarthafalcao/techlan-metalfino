from ..models import *
from django.db.models import Q
from login.models import User, UserComplement
from django.contrib.sessions.models import Session
from app.services.webservice import WebserviceSenior
from app.seniorSettings import *
from datetime import date, datetime
from re import search, compile


def validatePackages(packages:list) -> bool:
    '''valida embalagens de produção'''
    for package in packages: return package['qtdemb'] > 0
                 

def createPackages(prodReporting:dict, user:User):
    '''Cria embalagens de um apontamento de produção'''
    for package in prodReporting['embalagens']:
        createPackage(package, prodReporting, user)
        createHistoryPackage(package, prodReporting, 'A', user)

    
def createPackage(package:dict, prodReporting:dict, user:User):
    '''Cria uma embalagem no sistema Sapiens'''
    sitemb = 'F' if (package['coddep'] in ['00400', '00500']) else 'T'
    numemb = package['numemb'] if 'numemb' in package else getNextPackageNumber()
    veremb = getNextVersionPackage(numemb)
    Embalagem.objects.create(
        codemp=CODEMP,             
        numemb=numemb,        
        veremb=veremb,             
        coddep=package['coddep'],          
        sitemb=sitemb,           
        embdis="N",           
        codpro=package['codpro'],  
        codlot=prodReporting['codlot'],   
        qtdemb=package['qtdemb'],           
        etgatu=prodReporting['codetg'],             
        qtdini=package['qtdemb'],   
        datger=date.today(),
        horger=getCorrentHours(),
        usuger=user.codusu,
    )
    package.update({'numemb':numemb, 'veremb':veremb, 'codlot':prodReporting['codlot']})


def createHistoryPackage(package:dict, prodReporting:dict, typeHistory:str, user:User):
    '''Cria um novo histórico para uma embalagem'''
    seqhis = getNextSequenceHistory(package['numemb'], package['veremb'])
    HistoricoEmbalagem.objects.create(
        codemp=CODEMP,  
        numemb=package['numemb'],  
        veremb=package['veremb'],  
        seqhis=seqhis,  
        codori=prodReporting['codori'],  
        numorp=prodReporting['numorp'],  
        codetg=prodReporting['codetg'],  
        seqrot=prodReporting['seqrot'],  
        seqeoq=prodReporting['seqeoq'], 
        seqrfg=prodReporting['seqrfg'] if 'seqrfg' in prodReporting and prodReporting['seqrfg'] else None,
        codopr= prodReporting['codopr'],  
        codpro=package['codpro'],  
        codcre=prodReporting['codcre'],  
        codmol=prodReporting['codmol'] if 'codmol' in prodReporting else None,          
        codlot=prodReporting['codlot'],  
        qtdhis=package['qtdemb'],  
        tiphis=typeHistory,  
        numcad=prodReporting['numcad'],  
        depini=package['coddep'],  
        datger=date.today(),
        horger=getCorrentHours(),  
        usuger=user.codusu,  
        deprec=prodReporting['deprec'] if 'deprec' in prodReporting else None,  
        datrec=prodReporting['datrec'] if 'datrec' in prodReporting else None,          
        horrec=prodReporting['horrec'] if 'horrec' in prodReporting else None,          
        usurec=prodReporting['usurec'] if 'usurec' in prodReporting else None,          
        seqmov=prodReporting['seqmov'] if 'seqmov' in prodReporting else None        
    )
    Embalagem.objects.filter(numemb=package['numemb'], veremb=package['veremb'], codemp=CODEMP).update(hisatu=seqhis)


def printTags(listPackagesKeys:list, session:Session, printer:str):
    '''Imprime etiquetas de embalagens'''
    listValidsPackagesKeys = list(filter(lambda packageKey: Embalagem.objects.get(**packageKey), listPackagesKeys))
    numembList = ', '.join(list(map(lambda packageKey: str(packageKey['numemb']), listValidsPackagesKeys)))
    verembList = ', '.join(list(map(lambda packageKey: str(packageKey['veremb']), listValidsPackagesKeys)))

    seniorWS = WebserviceSenior(SENIOR_SERVER, session.get('usuario'), session.get('senha'))
    seniorWS.setPayload({
        "parameters": {
            "prEntrada": f"<ENumEmb={numembList}><EVerEmb={verembList}>",
            "prExecFmt": "tefPrint",
            "prPrintDest": printer,
            "prRelatorio": SENIOR_REPORT_TEMPLATE,
            "prEntranceIsXML": "F"
        },
        "wsdl": "g5-senior-services/sapiens_Synccom_senior_g5_co_ger_relatorio?wsdl",
        "porta": "Executar"
    })
    response = seniorWS.sendRequest()
    
    mensagem = handleMessage(response)
    if (not response or response.erroExecucao): 
        error = True
        for pacackeKey in listPackagesKeys: 
            if (pacackeKey in listValidsPackagesKeys): pacackeKey['printed'] = False
    else:
        error = False
        for pacackeKey in listPackagesKeys: 
            if (pacackeKey in listValidsPackagesKeys): pacackeKey['printed'] = True
    
    return {'error':error, 'message': mensagem}
    
    
def getPackage(codePackage:str) -> dict:
    '''Busca uma embalagem no banco de dados'''
    packageKeys = validateCodePackage(codePackage)
    if not packageKeys:
        raise ValueError("Código de pacote inválido.")
    try:
        package = Embalagem.objects.get(**packageKeys, codemp=CODEMP)
        historyPackage = HistoricoEmbalagem.objects.get(**packageKeys, codemp=CODEMP, seqhis = package.hisatu)
        return {
            'numemb': package.numemb,
            'veremb': package.veremb,
            'codpro': package.codpro,
            'codlot': package.codlot,
            'coddep': package.coddep,
            'desdep': package.related(Deposito).desdep,
            'sitemb': package.sitemb,
            'qtdemb': package.qtdemb,
            'histemb': {
                'codori': historyPackage.codori,
                'numorp': historyPackage.numorp
            }
        }
    except Embalagem.DoesNotExist:
        raise ValueError("Pacote não encontrado.")

def getNextPackageNumber() -> int:
    '''Retorna o próximo numero de embalagem disponível para uma data'''
    dateNum = int(date.today().strftime('%y%m%d'))
    Package = Embalagem.objects.filter(Q(numemb__icontains=dateNum), codemp=CODEMP).order_by('-numemb').values('numemb').first()
    if (not Package): return str(dateNum)+'0001' 
    nextSeqDate = int(str(Package['numemb']).replace(str(dateNum), '')) + 1
    return int(str(dateNum)+str(nextSeqDate).zfill(4))


def getNextVersionPackage(numemb:int) -> int:
    '''Retorna a versão da embalagem'''
    package = Embalagem.objects.filter(numemb=numemb, codemp=CODEMP).order_by('-veremb').values('veremb').first()
    return 1 if not package else int(package['veremb']) + 1


def getNextSequenceHistory(numemb: int, veremb: int) -> int:
    '''Retorna a próxima sequência de histórico para uma embalagem'''
    history = HistoricoEmbalagem.objects.filter(numemb=numemb, veremb=veremb, codemp=CODEMP).order_by('-seqhis').values('seqhis').first()
    return 1 if not history else int(history['seqhis']) + 1


def getCorrentHours()->int: return (datetime.now().hour * 60) + datetime.now().minute 


def handleMessage(response: dict) -> str:
    '''Trata mensagem de retorno do webservice Senior'''
    erroExecucao = response.erroExecucao
    if (erroExecucao):
        mensagem = search(r'"Sapiens - Gerais - Relatórios":\s*(.*)', erroExecucao)
        if mensagem: mensagem = mensagem.group(1)
        else: mensagem = erroExecucao
    else: mensagem = 'Etiquetas enviadas para impressão com sucesso!'
    return mensagem


def validateCodePackage(codePackage:str) -> dict:
    '''Valida o código de embalagem'''
    pattern = compile(r'^\d{8}\d+\.\d+$')
    validation = pattern.match(codePackage)
    if not bool(validation): return None
    return {'numemb':int(codePackage.split('.')[0]), 'veremb':int(codePackage.split('.')[1])}


def packageTransfer(packagesKey:list, origin:list, destination:str, session:Session, user:User) -> dict:
    '''Realiza o transferência de embalagens no sistema Sapiens'''
    packages = [Embalagem.objects.get(**key, codemp=CODEMP) for key in packagesKey]
    # Validações nas embalagens
    for package in packages: 
        if package.coddep == destination: return {'ok':False, 'message': "Embalagens já estão no depósito destino!"}
        if package.coddep != origin: return {'ok':False, 'message': f"Todas as embalagens precisam está no depósito {origin}!"}
        if package.sitemb != "T": return {'ok':False, 'message': f"Todas as embalagens precisam está com status <strong>A transferir</strong>!"}
    transferList = summarizePackages(packages)
    codccu = UserComplement.objects.get(codemp=CODEMP, codusu=user.codusu).codccu
    wsTransferList = []
    for transfer in transferList:
        transferLine = {
            'codEmp': CODEMP,
            'codFil': CODFIL,
            'codPro': transfer['produto'],
            'codDep': destination,
            'codDer': CODDER,     
            'codTns': CODTNS,
            'codLot': transfer['lote'],
            'qtdMov': transfer['quantidade'],
            'datMov': datetime.now().strftime('%d/%m/%Y'),
            'numDoc': transfer['op'],
            'codCcu': codccu,
            'oriOrp': transfer['origem'],
            'usuRes': user.codusu,
            'usuRec': user.codusu,
            'proTrf': transfer['produto'],
            'derTrf': CODDER,
            'depTrf': origin
        }
        wsTransferList.append(transferLine)
    
    seniorWS = WebserviceSenior(SENIOR_SERVER, session.get('usuario'), session.get('senha'))
    seniorWS.setPayload({
        "parameters": {
            "dadosGerais": wsTransferList,
            "processamentoBloco": "S"
        },
        "wsdl": "g5-senior-services/sapiens_Synccom_senior_g5_co_mcm_est_estoques?wsdl",
        "porta": "MovimentarEstoque_4"
    })
    response = seniorWS.sendRequest()
    # Associação do movimento a embalagem
    if response.tipoRetorno == 1:
        for package in packages:
            history = HistoricoEmbalagem.objects.get(numemb=package.numemb, veremb=package.veremb, seqhis=package.hisatu, codemp=CODEMP)
            seqmov = next(filter(lambda movimento: movimento.codPro == package.codpro 
                                         and movimento.oriOrp == history.codori 
                                         and movimento.numDoc == str(history.numorp)
                                         and movimento.codLot == package.codlot, response.retornoMovimento), None).seqMov
            Embalagem.objects.filter(codemp=CODEMP, numemb=package.numemb, veremb=package.veremb).update(coddep=destination, sitemb="R")
            HistoricoEmbalagem.objects.filter(codemp=CODEMP, numemb=package.numemb, veremb=package.veremb, seqhis=package.hisatu).update(
                deprec = destination,
                datrec = date.today(),
                horrec = getCorrentHours(),
                usurec = user.codusu,
                seqmov = seqmov)
        return {
            'ok': True,
            'message': 'Recebido com sucesso.',
            'coddep': destination,
            'desdep': Deposito.objects.get(codemp=CODEMP, coddep = destination).desdep
        }
    else:
        erros = []
        for i, transferRet in enumerate(response.retornoMovimento):
            if (transferRet.retorno != "OK"): 
                if transferRet.retorno not in erros: erros.append(transferRet.retorno)  
        
        return {
            'ok': False,
            'message': 'Erro: '+', '.join(erros),
           }
                
    
def reportingPackages(prodReporting:dict, user:User):
    '''Apontamento de embalagem'''
    for card in prodReporting['embalagens']:
        package = Embalagem.objects.get(codemp=CODEMP, numemb=card['numemb'], veremb=card['veremb'])
        balance = package.qtdemb - (card['qtdemb'] + card['qtdrfg']) * card['proportion']
        sitemb = 'F' if (card['coddep'] in ['00400', '00500']) else 'T'
        if (balance == 0): 
            createHistoryPackage(card, prodReporting, 'A', user)
            Embalagem.objects.filter(numemb=card['numemb'], veremb=card['veremb'], codemp=CODEMP
            ).update(coddep=card['coddep'], sitemb=sitemb, codpro=card['codpro'], etgatu=prodReporting['codetg'], qtdemb=card['qtdemb'])
        else:
            currentHistory = HistoricoEmbalagem.objects.filter(codemp=CODEMP, numemb=card['numemb'], veremb=card['veremb'], seqhis=package.hisatu).values().first()
            currentHistory['numcad'] = prodReporting['numcad']
            createHistoryPackage(
                {'numemb':package.numemb, 'veremb':package.veremb, 'codpro':package.codpro, 'qtdemb':balance, 'coddep':package.coddep},
                currentHistory, 'D', user)
            Embalagem.objects.filter(numemb=package.numemb, veremb=package.veremb, codemp=CODEMP                      
            ).update(embdis = 'S', qtdemb=balance)
            
            createPackage(card, prodReporting, user)
            createHistoryPackage(card, prodReporting, 'A', user)
            

            
        
        
     
def summarizePackages(packages:list) -> list:
    '''Sumariza embalagens por produto e lote'''
    summary = {}
    for package in packages:
        history = HistoricoEmbalagem.objects.get(numemb=package.numemb, veremb=package.veremb, seqhis=package.hisatu, codemp=CODEMP)
        key = f"{package.codpro}-{history.codori}-{history.numorp}-{package.codlot}"
        if(not key in summary):
            summary[key] = { 'produto': package.codpro, 'origem':history.codori, 'op':history.numorp, 'lote': package.codlot, 'quantidade': package.qtdemb }
            summary[key]['embalagens'] = [package]
        else: 
            summary[key]['quantidade'] += package.qtdemb
            summary[key]['embalagens'].append(package)
    
    return list(summary.values())
    