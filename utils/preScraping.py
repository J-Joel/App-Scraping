from apps.exchange.models import QuerysScripting
from typing import List

DOLAR_HOY: QuerysScripting = QuerysScripting(
    nombre_sitio = "Dolarhoy",
    url_target = "https://dolarhoy.com",
    user_agent = "BotPrueba",
    contenedor_selector="div.tile.is-parent.is-7.is-vertical > div.tile.is-child",
    # El modelo maneja este dict como JSONField
    campos_a_extraer = {
        "titulo": ".titleText",
        "compra": "div.compra > div.val",
        "venta": "div.venta-wrapper> div.val"
    }
)
# Para indicar el proximo elemento de un elemento es con ( ) o (>)
INFODOLAR: QuerysScripting = QuerysScripting (
    nombre_sitio = "InfoDolar",
    url_target = "https://www.infodolar.com",
    user_agent = "BotPrueba",
    contenedor_selector="table#DolarPromedio tr:has(td.colNombre)",
    # El modelo maneja este dict como JSONField
    campos_a_extraer = {
        "nombre": ".colNombre",
        "compra": "td.colCompraVenta:nth-child(2)",
        "venta": "td.colCompraVenta:nth-child(3)",
        "fecha": ".timeago.date"
    }
)

# Guarda las instancias en una lista, simula una BDD
LISTA_DE_CONFIGURACIONES_DOLAR: List[QuerysScripting] = [
    DOLAR_HOY,
    INFODOLAR,
]