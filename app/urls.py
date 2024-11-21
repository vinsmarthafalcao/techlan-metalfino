from django.urls import path, include

urlpatterns = [
    path('', include("login.urls")),
    path('apontamento/', include("apontamento.urls")),
    path('recebimento/', include("recebimento.urls")),
    path('apis/', include("apis.urls")),
]
