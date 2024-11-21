from app.services.webservice import WebserviceSenior
from app.seniorSettings import SENIOR_SERVER, CODEMP
from datetime import datetime
from ..models import OrdensProducao, RoteirosOP
from re import search

def toProdReporting(prodReporting:dict, session: dict):
    '''Realiza apontamento de produção no sistema Sapiens'''
    lote = prodReporting['codlot'] if 'codlot' in prodReporting else ""
    seniorWS = WebserviceSenior(SENIOR_SERVER, session.get('usuario'), session.get('senha'))
    try: qtdrfg = sumQtdPackages(prodReporting["embalagens"], "qtdrfg")
    except: qtdrfg = ""
    parameters = {
        "codOri": str(prodReporting["codori"]),
        "numOrp": str(prodReporting["numorp"]),
        "datIni": str(prodReporting["datini"]),
        "horIni": str(prodReporting["horini"]),
        "datRea": str(prodReporting["datrea"]),
        "horRea": str(prodReporting["horrea"]),
        "numCad": str(prodReporting["numcad"]),
        "codEtg": str(prodReporting["codetg"]),
        "codRot": str(prodReporting["seqrot"]),
        "codCre": str(prodReporting["codcre"]),
        "qtdRe1": str(sumQtdPackages(prodReporting["embalagens"], "qtdemb")),
        "qtdRfg": str(qtdrfg) if qtdrfg != "" and qtdrfg > 0 else "",
        "codLot": lote
    }

    if "codmol" in prodReporting: parameters["codMol"] = str(prodReporting["codmol"])

    seniorWS.setPayload({
        "parameters": parameters,
        "wsdl": "g5-senior-services/sapiens_Synccom_senior_g5_co_mpr_cha_movimentoop?wsdl",
        "porta": "ApontarOp"
    })

    response = seniorWS.sendRequest()
    if (not response): prodReporting.update({"erro": True, "retorno": "Erro ao apontar!", "seqEoq": 0})
    else: prodReporting.update({
            "codlot": response.codLot if 'codLot' in response else "",
            "codopr": RoteirosOP.objects.get(codemp = CODEMP, codori=prodReporting["codori"], numorp=prodReporting["numorp"], 
                                             codetg=prodReporting["codetg"], seqrot=prodReporting["seqrot"]).codopr,
            "seqeoq": response.seqEoq,
            "seqrfg": response.seqRfg if response.seqRfg != None and response.seqRfg > 0 else None,
            "erro": False if response.retorno == "OK" else True,
            "retorno": handleMessage(response),
        })


def sumQtdPackages(embalagens: list, tipqtd) -> int:
    '''Soma as quantidades das embalagens'''
    return sum([embalagem[tipqtd] for embalagem in embalagens])


def handleMessage(response: dict) -> str:
    '''Trata mensagem de retorno do webservice Senior'''
    erroExecucao = response.erroExecucao
    retorno = response.retorno
    if (erroExecucao):
        mensagem = search(r'ApontarOPs:\s*(.*)', erroExecucao)
        if mensagem: mensagem = mensagem.group(1)
        else: 
            mensagem = search(r'serviço " ":\s*(.*)', erroExecucao)
            if mensagem: mensagem = mensagem.group(1)
            else:  mensagem = erroExecucao
    else:  
        if (retorno == "OK"): mensagem = "Apontamento realizado com sucesso!"
        else: mensagem = retorno
    return mensagem

            
    




        