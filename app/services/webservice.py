from zeep import Client
from zeep.transports import Transport
from requests import Session

class WebserviceSenior:
    def __init__(self, server, usuario = "", senha = "") -> None:
        session = Session()
        self.transport = Transport(session=session)
        self.server = server
        
        # Montagem da requisição padrão SOAP
        if usuario and senha:
            self.Payload = {
                'user': usuario,
                'password': senha,
                'encryption': '0',
                'parameters': {}
            }
        else:
            self.Payload = {
                'parameters': {}
            }
    
    # Definição dos parâmetros de cada webservice
    def setPayload(self, payload):
        self.wsdl = self.server+"/"+payload["wsdl"]
        self.porta = payload["porta"]
        self.Payload['parameters'] = payload['parameters']
    
    # Envio da requisição SOAP    
    def sendRequest(self) -> dict:
        try:
            self.client = Client(wsdl=self.wsdl, transport=self.transport)
            response = self.client.service[self.porta](**self.Payload)
            return response
        except Exception as e:
            print(e)
