from django.urls import path
from .views import *


urlpatterns = [
    path("listaProdutos", listaProdutos, name="listaProdutos"),
    path("listaOrigens", listaOrigens, name="listaOrigens"),
    path("listaCentroRecursos", listaCentroRecursos, name="listaCentroRecursos"),
    path("listaOperadores", listaOperadores, name="listaOperadores"),
    path("listaMoldes", listaMoldes, name="listaMoldes"),
    path("listaOps", listaOps, name="listaOps"),
    path("getDataOp", getDataOp, name="getDataOp"),
    path("getPackage", getPackageView, name="getPackage"),
    path("getDepositDestination", getDepositDestination, name="getDepositDestination")
]