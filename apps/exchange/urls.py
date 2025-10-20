from django.urls import path
from . import views

urlpatterns = [
    path("/dolarHoy", views.DolarHoy, name="dolarHoy"),
    
    #API
    path("/resultados", views.ValorDolar, name="resultados"),
]