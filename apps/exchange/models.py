from django.db import models

# Create your models here.
class QuerysScripting(models.Model):
    nombre_sitio = models.CharField('nombre_sitio',max_length=100)
    url_target = models.URLField('url_target',max_length=255,help_text="URL objetivo para el scraping.")
    user_agent = models.CharField('user_agent',max_length=100,help_text="Nombre del bot a scrapear.")
    contenedor_selector = models.CharField('contenedor_selector',max_length=255,help_text="Contenedor que contiene los datos a extraer.")
    campos_a_extraer = models.JSONField('campos_a_extraer',help_text="Diccionario JSON de selectores.")

    def __str__(self):
        # Define la representación en texto del objeto (útil en el Admin)
        return self.nombre_sitio

    class Meta:
        verbose_name = "Configuración de Scraping"
        verbose_name_plural = "Configuraciones de Scraping"