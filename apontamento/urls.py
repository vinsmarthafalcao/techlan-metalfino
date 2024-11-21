from django.urls import path
from . import views


urlpatterns = [
    path("injecao", views.noteProduction_INJ, name="apt_injecao"),
    path("geral", views.noteProduction_GERAL, name="apt_geral"),
    path("imprimirEmbalagens", views.printTagsPackages, name="imprimirEmbalagens"),
]