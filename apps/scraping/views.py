from django.shortcuts import render

# Imports de API
from utils.scraping import es_seccion_scrapeable, realizar_scraping
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from typing import Dict, Any

# Create your views here.
def InfoScraping(request):
    return render(request, 'scraping/info.html')

def PaginaScrapeable(request):
    return render(request, 'scraping/seccionPermitida.html')

def PaginaNoScrapeable(request):
    return render(request, 'scraping/seccionNoPermitida.html')

def HerramientaScraping(request):
    return render(request, 'scraping/herramienta.html')

# ----------------------------------------------------
# API SCRAPING
# ----------------------------------------------------
@api_view(['GET'])
def VerificarRobots(request) -> Response:
    """
    Endpoint GET que ejecuta la lógica de verificación de robots.txt usando la función es_seccion_scrapeable.
    
    Devuelve un JSON siendo los parametros importantes: 
        scrapeo_permitido: TRUE | TRUE | FALSE
        codigo_resultado: PERMITIDO | NO_ENCONTRADO | DENEGADO
    """
    # Leer los parámetros de entrada de la URL
    target_url = request.query_params.get('target_url')
    user_agent = request.query_params.get('user_agent')

    # Validar parámetros
    if not target_url or not user_agent:
        return Response({
            "error": "Faltan parámetros",
            "detalles": "Se requieren 'target_url' y 'user_agent'."
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Ejecutar la lógica de verificación
    try:
        # La función devuelve True PERMITIDO o True NO_ENCONTRADO o False DENEGADO
        es_permitido, codigo_resultado = es_seccion_scrapeable(target_url, user_agent)

        # Construir la respuesta final
        datos_respuesta: Dict[str, Any] = {
            "estado": "éxito",
            "url_verificada": target_url,
            "agente_usado": user_agent,
            "scrapeo_permitido": es_permitido,
            "codigo_resultado": codigo_resultado,
            "mensaje": "La URL está permitida para el User-Agent especificado." if es_permitido else "La URL está DENEGADA por robots.txt."
        }
        
        # Devolver 200 OK con el resultado
        return Response(datos_respuesta, status=status.HTTP_200_OK)
    
    # Manejo de errores internos (ej. URL mal formada que cause un error de parsing)
    except Exception as e:
        return Response({
            "error": "Error interno al procesar la verificación",
            "detalles": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def iniciar_scraping_api(request) -> Response:
    """
    Endpoint POST que ejecuta el scraping estructurado, recibiendo:
        URL
        User-Agent
        Contenedor selector (con instrucciones HTML-CSS)
        Campos a extraer (con instrucciones HTML-CSS, cada uno).
    Devuelve un JSON, devolviendo lo scrapeado en el parametro resultados como una lista de diccionarios
    """

    # 1. Obtener datos dinámicos del cuerpo POST (JSON)
    target_url = request.data.get('target_url')
    user_agent = request.data.get('user_agent')
    contenedor_selector = request.data.get('contenedor_selector') 
    campos_a_extraer = request.data.get('campos_a_extraer') # Debe ser un diccionario

    # Validación de Parámetros
    if not all([target_url, user_agent, contenedor_selector, campos_a_extraer]):
        return Response({
            "error": "Parámetros incompletos",
            "detalles": "target_url, user_agent, contenedor_selector, y campos_a_extraer son obligatorios."
        }, status=status.HTTP_400_BAD_REQUEST)
    
    es_permitido, codigo_resultado = es_seccion_scrapeable(target_url, user_agent)

    # Verifica que el scrapeo este permitido
    if not(es_permitido):
        return Response({
            "estado": "error_scraping",
            "mensaje": "Scraping denegado por robots.txt.",
        }, status=status.HTTP_403_FORBIDDEN)
    
    # Crear la estructura de selectores requerida por la función de utilidad
    selectores_dinamicos = {
        "contenedor_item": contenedor_selector,
        "campos_internos": campos_a_extraer
    }

    # Ejecutar la función de utilidad de scraping
    try:
        datos_extraidos = realizar_scraping(
            url = target_url, 
            user_agent = user_agent, 
            selectores = selectores_dinamicos
        )
        
        # Devolver la lista de diccionarios extraída
        return Response({
            "estado": "éxito",
            "resultados": datos_extraidos
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            "estado": "error_scraping",
            "mensaje": "Fallo la extracción de datos, sitio web no disponible.",
            "detalles": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
