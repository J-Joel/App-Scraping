$(document).ready(function() {
    // Se instancia y identifica los elementos
    const $urlInput = $('#urlInput');
    const $userAgentInput = $('#userAgentInput');
    const $statusMessage = $('#statusMessage');
    const $contenedorSelectorInput = $('#contenedorSelectorInput');
    const $camposAExtraerInput = $('#camposAExtraerInput');
    const $btnScraping = $('#btnScraping');
    const $urlForm = $('#urlForm');

    // Temporizador para la verificacion del robot.txt
    let debounceTimer; 

    // Funcion para actualizar el cartel de mensaje
    function updateStatus(isAllowed, message) {
        $statusMessage.removeClass('hidden message-allowed message-denied');
        
        $statusMessage.text(message);
        
        if (isAllowed) {
            $statusMessage.addClass('message-allowed');
            $statusMessage.show();
        } else {
            $statusMessage.addClass('message-denied');
            $statusMessage.show();
        }
    }

    // Función para limpiar y ocultar el mensaje
    function hideStatus() {
        $statusMessage.addClass('hidden').empty();
    }

    // Función de verificación de robot.txt
    function verificarUrl(url, userAgent) {
        $btnScraping.prop('disabled', true); 
        hideStatus();
        
        // Si falta la URL o el User-Agent
        if (!url || url.length < 5 || !userAgent) {
            return;
        }

        $.ajax({
            url: 'http://127.0.0.1:8000/scraping/verificacion',
            method: 'GET',
            data: { 
                target_url: url,
                user_agent: userAgent
            },
            timeout: 5000, 
            
            success: function(response, textStatus, xhr) {
                if (xhr.status === 200 && response.codigo_resultado == "PERMITIDO" && response.scrapeo_permitido) {
                    // La solicitud fue exitosa (200) Y el resultado de la lógica de robots es TRUE
                    console.log(`Verificación exitosa para ${userAgent}. Botón habilitado.`);
                    $btnScraping.prop('disabled', false);
                    updateStatus(true, "Scraping PERMITIDO.");
                }
                else if (xhr.status === 200 && response.codigo_resultado == "NO_ENCONTRADO") {
                    // Si el estado no es 200 o si el servidor dijo que el scrapeo está NO_ENCONTRADO (false)
                    console.log(`Verificación exitosa para ${userAgent}. Botón habilitado.`);
                    $btnScraping.prop('disabled', false);
                    updateStatus(false, "Archivo robots.txt no encontrado. Asumiendo permiso.");
                }
                else if (xhr.status === 200 && response.codigo_resultado == "DENEGADO") {
                    // Si el estado no es 200 o si el servidor dijo que el scrapeo está DENEGADO (false)
                    console.warn(`Verificación exitosa, pero scrapeo DENEGADO o error menor.`);
                    $btnScraping.prop('disabled', true);
                    updateStatus(false, "Scraping DENEGADO por robots.txt.");
                }
            },
            
            error: function(xhr, status, error) {
                console.error(`Verificación fallida. Estado: ${xhr.status}`);
                $btnScraping.prop('disabled', true);
                updateStatus(false, "Error de conexión o servidor. Intenta de nuevo.");
            }
        });
    }

    // Evento
    function handleInputChange() {
        clearTimeout(debounceTimer); 
        const url = $urlInput.val().trim();
        const userAgent = $userAgentInput.val().trim();
        
        // Si ambos campos están vacíos, oculta el mensaje
        if (!url && !userAgent) {
            hideStatus();
            $btnScraping.prop('disabled', true);
            return;
        }
        // Establecer un nuevo temporizador
        debounceTimer = setTimeout(() => {
            verificarUrl(url, userAgent);
        }, 400);
    }

    // Se añade los eventos a los elementos
    $urlInput.on('input', handleInputChange);
    $userAgentInput.on('input', handleInputChange);

    // Capturar el evento submit del formulario
    $urlForm.on('submit', function(e) {
        e.preventDefault(); // Evita que el formulario se envíe de la manera tradicional (recarga de página)
        
        $btnScraping.prop('disabled', true).text('Procesando...');

        const target_url = $urlInput.val().trim();
        const user_agent = $userAgentInput.val().trim();
        const contenedor_selector = $contenedorSelectorInput.val().trim();
        
        // El campo de campos_a_extraer debe ser parseado como JSON
        let campos_a_extraer_json;
        try {
            campos_a_extraer_json = JSON.parse($camposAExtraerInput.val().trim());
        } catch (error) {
            alert('Error: La estructura de Campos a Extraer no es JSON válido.');
            $btnScraping.prop('disabled', false).text('Enviar Solicitud POST');
            return;
        }

        // Construir el objeto de datos que se enviará en el cuerpo (body) del POST
        const postData = {
            target_url: target_url,
            user_agent: user_agent,
            contenedor_selector: contenedor_selector,
            campos_a_extraer: campos_a_extraer_json
        };

        // Petición POST con $.ajax()
        $.ajax({
            url: "http://127.0.0.1:8000/scraping/scrapearPagina",
            method: 'POST',
            contentType: 'application/json', // Informa al servidor que estamos enviando JSON
            data: JSON.stringify(postData),   // Convertir el objeto JS a una cadena JSON
            
            success: function(response) {
                // Manejo de respuesta exitosa del POST (ej. 200 OK)
                console.log("Scraping Finalizado:", response);
                alert('Scraping Finalizado. Resultados en la consola.');
                $btnScraping.prop('disabled', false).text('Enviar Solicitud POST');
            },
            
            error: function(xhr, status, error) {
                // Manejo de errores (4xx, 5xx, etc.)
                let errorMsg = xhr.responseJSON ? xhr.responseJSON.mensaje : 'Error desconocido al iniciar scraping.';
                console.error("Error POST:", errorMsg);
                alert(`Fallo en el POST: ${errorMsg}`);
                $btnScraping.prop('disabled', false).text('Enviar Solicitud POST');
            }
        });
    });
});