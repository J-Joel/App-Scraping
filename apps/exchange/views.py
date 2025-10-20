from django.shortcuts import render
from utils.preScraping import LISTA_DE_CONFIGURACIONES_DOLAR

# Imports de API
from rest_framework.decorators import api_view
from rest_framework.response import Response

def DolarHoy(request):
    lista_paginas = LISTA_DE_CONFIGURACIONES_DOLAR
    return render(request, 'exchange/dolarHoy.html', {"paginas":lista_paginas})

@api_view(['POST'])
def ValorDolar(request):
    """
    EndPoint: Recibe los resultados del scraping (JSON) y devuelve una vista parcial HTML, con los datos ya estructurados en formato tabla.
    """
    try:
        # request={"estado": "éxito", "resultados": Array(...)}
        resultados = request.data.get('resultados', [])
        return render(request, 'exchange/_resultadosPage.html', {"resultados":resultados})

    except Exception as e:
        # Devuelve un fragmento de error
        return Response(f'<p class="error-message">Error al renderizar los datos: {str(e)}</p>', 
                        status=400, content_type='text/html')

