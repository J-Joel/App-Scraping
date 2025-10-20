import requests
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser as RP
from typing import Tuple, Dict, Union, Any, List
from bs4 import BeautifulSoup

# ----------------------------------------------------
# CACHÉ GLOBAL DE ROBOTS.TXT
# Almacena objetos RobotFileParser ya configurados por dominio (netloc) para evitar descargas y parsing repetidos.
# ----------------------------------------------------
# Se podria almacenar los robots.txt a una base de datos, en ese caso se debe de verificar los cambios del robots.txt
ROBOTS_PARSER_CACHE = {}

# ----------------------------------------------------
# FUNCIÓN DE ORGANIZACION
# ----------------------------------------------------
def flush_block(agent, block) -> str:
    """
    Reestructura las reglas desordenadas de un User-Agent:
        User-agent
        Disallow
        Allow
        etc.
    Esta es la estructura basica y utilizada por la libreria RobotParser,
    en caso de no reestructurar el robots.txt, se cometera errores de lectura por parte de sus funciones
    """
    reorganized = ""
    if agent:
        reorganized += f"User-agent: {agent}\n"
    
    # Escribir Disallows
    for line in block.get('Disallow', []):
        reorganized += line + "\n"
    # Escribir Allows
    for line in block.get('Allow', []):
        reorganized += line + "\n"
    # Escribir Otros (Crawl-delay, Sitemap, etc.)
    for line in block.get('Other', []):
        reorganized += line + "\n"
    return reorganized.strip()

def reorganizar_robots_txt(content: str) -> str:
    """
    Toma el contenido original del robots.txt, acumula todas las reglas por 
    User-agent único y las reorganiza en un solo bloque por agente.

    Maneja la acumulación de reglas para múltiples User-agents seguidos.
    Maneja la repeticion de User-agents.
    """
    lines = content.splitlines()
    # Almacenamiento acumulativo de todas las reglas de todos los agentes.
    # { { Agente :{'Disallow': [], 'Allow': [], 'Other': []} }, }
    all_agents_rules = {} 
    
    # Grupo de agentes activos a los que se aplicará la siguiente regla.
    # [ Agente, Agente, ...]
    current_agent_group = [] 
    
    # Flag para manejar la agrupación de agentes consecutivos
    last_line_was_user_agent = False 

    for line in lines:
        cleaned_line = line.strip()
        if not cleaned_line or cleaned_line.startswith('#'):
            last_line_was_user_agent = False # Resetea el flag si es una línea vacía/comentario
            continue 
        

        # Si se lee un nuevo User-agent
        if cleaned_line.lower().startswith("user-agent:"):
            agent_name = cleaned_line[len("user-agent:"):].strip()
            
            # Si la línea anterior NO fue un User-agent (o si el grupo estaba vacío),
            # significa que el bloque anterior terminó, así que reiniciamos el grupo.
            if not last_line_was_user_agent:
                current_agent_group = [] 
            
            # Añadir el nuevo agente al grupo activo (consecutivo o nuevo).
            current_agent_group.append(agent_name)
            
            # Inicializar su estructura de reglas si es la primera vez que aparece
            if agent_name not in all_agents_rules:
                all_agents_rules[agent_name] = {'Disallow': [], 'Allow': [], 'Other': []}
            
            last_line_was_user_agent = True
            continue
        
        # Si es una línea de regla o directiva, termina la secuencia de User-agents.
        is_rule_line = False
        lower_line = cleaned_line.lower()
        rule_type = None

        if lower_line.startswith("disallow:"):
            rule_type = 'Disallow'
            is_rule_line = True
        elif lower_line.startswith("allow:"):
            rule_type = 'Allow'
            is_rule_line = True
        elif lower_line.startswith("crawl-delay:"):
            rule_type = 'Other'
            is_rule_line = True

        if is_rule_line:
            # Si encontramos una regla, la aplicamos a CADA agente en el grupo actual.
            if current_agent_group:
                for agent_name in current_agent_group:
                    # ACUMULACIÓN: La regla se añade para todos los agentes en el grupo
                    if agent_name in all_agents_rules:
                        all_agents_rules[agent_name][rule_type].append(cleaned_line)
            # Una vez que se aplica la regla, el flag de User-agent debe ser FALSE
            # para que el próximo User-agent reinicie el grupo.
            last_line_was_user_agent = False
        
        # Resto de líneas que no son reglas
        elif not is_rule_line:
            last_line_was_user_agent = False
    
    # Escribir la Salida Final (Solo un bloque por agente)
    robotReorganizado = ""
    for agente, reglas in all_agents_rules.items():
        # Llama a flush_block una vez para el agente, con todas sus reglas acumuladas.
        robotReorganizado += flush_block(agente, reglas) + "\n\n"
    
    # print(reorganized_output)
    return robotReorganizado.strip()

# ----------------------------------------------------
# FUNCIÓN PRINCIPAL DE VERIFICACIÓN
# ----------------------------------------------------
def es_seccion_scrapeable(url_completa: str, user_agent: str) -> Tuple[bool, str]:
    """
    Verifica si una URL está permitida para un User-Agent específico,
    usando caching y reordenando el robots.txt si es necesario.
    """
    
    parsed_url = urlparse(url_completa)
    netloc = parsed_url.netloc # Dominio, usado como clave de caché
    
    # Comprobar caché
    if netloc in ROBOTS_PARSER_CACHE:
        rp = ROBOTS_PARSER_CACHE[netloc]
        print(f"INFO: Usando robots.txt de caché para {netloc}")
    else:
        # Si no está en caché, inicializar el parser y descargar
        robots_url = f"{parsed_url.scheme}://{netloc}/robots.txt"
        rp = RP()
        
        try:
            response = requests.get(robots_url, timeout=5, headers={'User-Agent': user_agent})
            
            # Verificar errores HTTP (4xx o 5xx)
            response.raise_for_status() 

            # Reorganizar el contenido para corregir el orden de Allow/Disallow
            robotReorganizado = reorganizar_robots_txt(response.text)
            
            # Alimentar el contenido REORGANIZADO al parser.
            rp.parse(robotReorganizado.splitlines())
            
            # Guardar en caché para futuras llamadas
            ROBOTS_PARSER_CACHE[netloc] = rp
            
        # Si hay un error de conexión, 404, o 500, asumimos permiso por defecto
        except requests.exceptions.RequestException:
            print(f"Advertencia: Fallo al descargar robots.txt. Asumiendo permiso.")
            return True, "NO_ENCONTRADO"

    # Extracción de la ruta
    ruta_a_verificar = parsed_url.path

    # Se agrega parametros de busqueda
    if parsed_url.query:
        ruta_a_verificar += f"?{parsed_url.query}"
    
    # Diagnóstico e Imprime el resultado de la lógica de precedencia
    # delay = rp.crawl_delay(user_agent)
    # print(f"Diagnóstico: Crawl-Delay para {user_agent}: {delay}. Reglas cargadas.")
    
    # Verificar el acceso
    resultado = rp.can_fetch(user_agent, ruta_a_verificar)
    codigo_resultado = "PERMITIDO" if resultado else "DENEGADO"
    print(f"Resultado para {url_completa} ({user_agent}): {codigo_resultado}")

    return resultado, codigo_resultado

# ----------------------------------------------------
# FUNCIÓN PRINCIPAL DE SCRAPING
# Puede mejorar todavía
# ----------------------------------------------------
def realizar_scraping(url: str, user_agent: str, selectores: Dict[str, Union[str, Dict[str, str]]]) -> Dict[str, Any]:
    """
    Descarga el contenido de la URL y extrae una lista de diccionarios, 
    donde cada diccionario representa un ítem completo.
    """
    headers = {'User-Agent': user_agent}
    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status() 
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Obtener el selector del contenedor y los campos internos
    contenedor_selector = selectores.get("contenedor_item")
    campos_internos = selectores.get("campos_internos", {})
    
    if not contenedor_selector:
        # Retorna una lista vacía si no se define el contenedor
        return [{"error": "Selector de contenedor principal no definido."}]
    
    # Buscar TODOS los contenedores
    contenedores = soup.select(contenedor_selector)
    
    # Lista final donde se almacenará cada diccionario de ítem
    lista_de_items: List[Dict[str, Any]] = []
    
    # Iterar sobre cada contenedor encontrado
    for contenedor in contenedores:
        item_data: Dict[str, Any] = {}
        
        # Para cada contenedor, buscar sus campos internos
        for clave, selector_relativo in campos_internos.items():
            
            # Buscar el elemento DENTRO del contenedor actual
            elemento = contenedor.select_one(selector_relativo) 
            
            # Logica de lectura de elementos
            if elemento:
                valor = None

                if elemento.name == 'a':
                    # Si es un enlace, capturamos AMBOS: texto y href
                    valor = {
                        "texto": elemento.text.strip(),
                        "href": url+elemento.get('href')
                    }
                elif elemento.get('data-order'):
                    valor = elemento.get('data-order')
                # Extraer texto o atributo (ej. 'src' para imágenes)
                elif elemento.get('href'):
                    valor = elemento.get('href')
                elif elemento.get('src'):
                    valor = elemento.get('src')
                else:
                    valor = elemento.text.strip()
                
                item_data[clave] = valor
            else:
                item_data[clave] = "No encontrado"
        
        # Agregar el diccionario del ítem completo a la lista
        if item_data:
            lista_de_items.append(item_data)

    return lista_de_items