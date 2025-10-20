from django.urls import path
from . import views

urlpatterns = [
    path("", views.Inicio, name="inicio"),
    path('robots.txt', views.robots_txt, name='robotstxt'),
]