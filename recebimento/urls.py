from django.urls import path
from . import views


urlpatterns = [
    path("", views.receipt_view, name="recebimento"),
]