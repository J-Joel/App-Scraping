from django.urls import path
from . import views

urlpatterns = [
    path("", views.InfoScraping, name="infoScraping"),
    path("/zonaPermitida", views.PaginaScrapeable, name="zonaPermitida"),
    path("/zonaNoPermitida", views.PaginaNoScrapeable, name="zonaNoPermitida"),
    path("/herramientaScraping", views.HerramientaScraping, name="herramientaScraping"),
    
    # URLs API
    path('/verificacion', views.VerificarRobots, name='verificacion'),
    path('/scrapearPagina', views.iniciar_scraping_api, name='scrapingPag'),
]