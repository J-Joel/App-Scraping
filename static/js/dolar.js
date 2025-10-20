$(document).ready(function() {
    const $select = $('#selectorQuery');
    const $detallesDiv = $('#datosExtraidos');

    // Evento 'change' en el input selector
    $select.on('change', function() {
        const $selectedOption = $(this).find('option:selected');
        const configId = $(this).val();
        if (!configId) {
            $detallesDiv.hide().empty();
            return;
        }
        $detallesDiv.html('<p>Cargando detalles...</p>').show();
        const target_url = $selectedOption.data('url');
        const user_agent = $selectedOption.data('agent');
        const contenedor_selector = $selectedOption.data('selector');
        
        // Manejar el JSON del data-datos de Js a Json
        const datos_json_js = $selectedOption.data('datos');
        const datos_json = datos_json_js.replace(/'/g, '"')
        let campos_a_extraer;

        try {
            // El JSONField de Django se serializa como cadena, hay que parsearlo
            campos_a_extraer = JSON.parse(datos_json); 
        } catch (e) {
            console.error("Error al parsear el JSON de campos a extraer:", e);
            alert("Error: El formato de los campos de extracción es inválido.");
            $detallesDiv.html('<p class="error-message">Error en la configuración JSON.</p>');
            return;
        }
        
        const postData = {
            target_url: target_url,
            user_agent: user_agent,
            contenedor_selector: contenedor_selector,
            campos_a_extraer: campos_a_extraer // Ya es un objeto JSon
        };
        
        console.log("Datos a enviar (POST):", postData);
        $.ajax({
            url: "http://127.0.0.1:8000/scraping/scrapearPagina",
            method: 'POST',
            contentType: 'application/json', // Informa al servidor que estamos enviando JSON
            data: JSON.stringify(postData),   // Convertir el objeto JS a una cadena JSON
            dataType: 'json', // Esperamos JSON de la vista de Scraping
            
            success: function(response) {
                $.ajax({
                    url: "http://127.0.0.1:8000/exchange/resultados",
                    method: 'POST',
                    contentType: 'application/json',
                    data: JSON.stringify(response),
                    dataType: 'html', // Esperamos HTML de esta vista
                    
                    success: function(htmlResponse) {
                        // Inyectamos el HTML
                        $detallesDiv.html(htmlResponse); 
                    },
                    
                    error: function(xhrRender) {
                        $detallesDiv.html('<p class="error-message">Error al convertir los resultados a HTML.</p>');
                        console.error("AJAX Render Error:", xhrRender.responseText);
                    }
                });
            },
            
            error: function(xhrScraping) {
                $detallesDiv.html('<p class="error-message">Error al ejecutar el scraping.</p>');
                console.error("AJAX Scraping Error:", xhrScraping.responseText);
            },
        });
    });
});