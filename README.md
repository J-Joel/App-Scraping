# App-Scraping
<div align="center">
  <img src="./static/img/pre.gif" width="50%" height="50%"/>
</div>

## **Descripcion**

En este repositorio se tendrá a disposición información sobre el scraping y una herramienta básica dedicada a esta actividad, todo esto desarrollada en Python.

## **Instrucciones de instalacion**

Para poder ejecutar instalar y ejecutar este repositorio se debe clonar a través de Git o descargarlo como ZIP (y luego extraerlo).

**(1) Creacion de entorno**: 

Una vez bajado el repositorio, ubíquese en la carpeta raíz del repositorio (App-Scraping), donde se encuentra el archivo manage.py. En esa ubicacion, se debe de abrir la terminal para acto seguido crear un entorno virtual para la aplicacionm ejecutando el comando:

```bash
    py -m venv [nombre_del_entorno]
```
*Se recomienda usar "venv" como nombre para el entorno.*

**(2) Iniciar entorno**: 

Ya creado el entorno, se le puede iniciar mediante el archivo: "activate", ubicado en la carpeta venv/Scripts/, para ello se ejecuta el comando desde la raiz del proyecto:

Linux/macOS (Bash/Zsh):
``` bash
    source venv/Scripts/activate
```
Windows (CMD/PowerShell):
``` bash
    .\venv\Scripts\activate
```
*Si el entorno se activó correctamente, lo notará al ver el nombre de su entorno entre paréntesis en la terminal.*

**(3) Intalar dependicias**: 

Asegúrese de encontrarse en la carpeta raíz (.../App-Scraping). Instale las librerías y frameworks listados en el archivo requirements.txt con el siguiente comando:

``` bash
    pip install -r requirements.txt
```
*Asegúrese de contar con conexión a internet al ejecutar este comando.*

**(4) Iniciar el proyecto**: 

Con todos los procedimientos realizados, el proyecto estará listo para ejecutarse con el siguiente comando:

``` bash
    py manage.py runserver [puerto]
```
*Si no se define un puerto, el servidor se ejecutará por defecto en el puerto 8000*

## **Librerias utilizadas**:
Todas las librerias utilizadas completamente, se encuentra en el archivo "requirements.txt"

**Frontend: JavaScript**:

- Jquery
  
**Backend: Python**:
  
- Django
- Python-DotEnv *(Para variables de entorno, no se implemento)*
  
**Api**:
  
- DjangoRest
- Python-DotEnv *(Para variables de entorno, no se implemento)*
- BeautifulSoup4 *(Funciones de scraping)*
- Requests *(Para la obtencion de los archivos Robots.txt)*
- RobotParser *(Para el parseo de Robots.txt)*

*Nota: Este repositorio está construido como un proyecto único de Django monolítico. Sin embargo, los métodos REST podrían separarse en un proyecto dedicado de API para una arquitectura de microservicios.*

## **Logica de negocio sobre scraping**

Para la extracción específica de una estructura de datos de una determinada página, se debe consultar el archivo robots.txt, en la cual podremos saber si la direccion a la que queremos scrapear, contamos con los permisos necesarios de realizar dicha actividad, para evitar negaciones o prohibiciones por parte del sitio.

Con los permisos comprobados y verificados, ya sea uno mismo o el algoritmo utilizado para esta tarea, se procede con la obtención del HTML de la página, en la cual a partir de los respectivos parametros de busqueda, podremos definir el patrón de diseño repetitivo (selector) que contiene los datos a extraer mediante una instruccion, como tambien definiendo los parametros a extraer mediante una extructura: clave e instrucción. Estas instrucciones son enteramente elementos HTML, atributos y CSS, de la cual podremos ayudarnos con la herramienta de inspeccion que trae cada navegador web.

El algoritmo encargado de buscar los elementos, se encarga de leer el HTML en busca del elemento selector (o contenedor) de los datos, ya que estos contenedores son frecuentemente repetitivos, lo que permite la reutilización de clases CSS y facilita la búsqueda. Apartir de esos selectores, el algoritmo identifica los campos a extraer, segun la estructura de datos que se haya definido para buscar.
Una vez finalizado la lectura o parseo, devolverá su valor en formato JSON (para la consola/API) o en una vista parcial (Exchange), para su presentación dinámica en pantalla.
