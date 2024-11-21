from django.contrib.auth.backends import BaseBackend
from app.services.webservice import WebserviceSenior
from login.models import User
from django.http import HttpRequest
from django.shortcuts import redirect
from django.contrib.sessions.models import Session
from django.contrib.auth import get_user_model
from django.utils import timezone 
from app.seniorSettings import SENIOR_SERVER

class SeniorBackend(BaseBackend):
    # autentica um usuário usando webservice Senior
    def authenticate(self, request, username=None, password=None):
        # Requisição de webservice para autenticação do usuário na Senior
        wsLogin = WebserviceSenior(SENIOR_SERVER, username, password)
        wsLogin.setPayload({
            "parameters": {
                "pmUserName": username,
                "pmUserPassword": password,
                "pmEncrypted": 0
            },
            "wsdl": "g5-senior-services/sapiens_SyncMCWFUsers?wsdl",
            "porta": "AuthenticateJAAS"
        })
        response  = wsLogin.sendRequest()
        
        # Verificar a resposta do serviço externo
        if response["pmLogged"] == '0': 
            # instancia usuário e senha para requisições futuras de wbeservice
            request.session['usuario'] = username
            request.session['senha'] = password
            user = User.objects.get(nomusu=username)
            return user
    
        return None
    
# retorna dados da sessão se houver
def getDataSession(request:HttpRequest) -> Session:
    try:
        session_key = request.COOKIES["sessionid"]
        session = Session.objects.get(session_key=session_key, expire_date__gte=timezone.now())
        return session.get_decoded()
    except:
        return None
    

# retorna usuário da sessão se houver
def getUserSession(session:Session) -> User:
    try:
        user_id = session.get('_auth_user_id')
        if user_id:
            User = get_user_model()
            return User.objects.get(pk=user_id)
        else: return None
    except: return None
            
    
    
# Decorator para validar sessão
def require_authentication(view_func):
    def wrapper(request: HttpRequest, *args, **kwargs):
        user = getUserSession(getDataSession(request))
        if not user: return redirect('login')
        if user.is_authenticated: return view_func(request, *args, **kwargs)  
        else: return redirect('login')
    return wrapper
   