from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.staticfiles import finders

def Inicio(request):
    return render(request, 'home/index.html')

def robots_txt(request):
    robots_path = finders.find('robots.txt')
    
    if robots_path:
        # ✅ Abrir con codificación explícita
        with open(robots_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # ✅ Usar HttpResponse con Content-Type correcto
        return HttpResponse(content, content_type="text/plain; charset=utf-8")
    
    # Caso de fallback (si el archivo no se encuentra)
    # Devolver un robots.txt que no permita nada por seguridad o un mensaje claro.
    return HttpResponse("User-agent: *\nDisallow: /", content_type="text/plain")