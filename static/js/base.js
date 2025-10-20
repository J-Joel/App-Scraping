const elementos = document.querySelectorAll(".nav-link"); // Lee los elementos que tiene la clase: nav-link

elementos.forEach(elemento => { // Por cada elemento del array
    elemento.addEventListener("mousemove", (e) => { // Añade el evento: mousemove
        const { x, y } = elemento.getBoundingClientRect();
        elemento.style.setProperty("--x", (e.clientX - x)+"px");
        elemento.style.setProperty("--y", (e.clientY - y)+"px");
    });
});
$(document).ready(function() {
    const $titulo = $('#tituRedi');
    const $tooltip = $('#custom-tooltip');

    $titulo.on('click', function() {
        
        // 1. Obtener la URL del atributo data-url usando .data()
        // jQuery convierte 'data-url' a 'url' automáticamente.
        const urlDestino = $(this).data('url'); 
        
        // (Alternativa: usar .attr())
        // const urlDestino = $(this).attr('data-url');
        
        if (urlDestino) {
            // 2. Redireccionar
            window.location.href = urlDestino;
        } else {
            console.error("Error: El atributo data-url está vacío.");
        }
    });
    
    // Seleccionar todos los inputs y textareas que tienen datos para el tooltip
    $('input[data-info], textarea[data-info]').on('mouseenter', function(e) {
        const infoText = $(this).data('info');
        
        // Preparar el contenido HTML (usando '|' como separador de línea)
        const infoLines = infoText.split('|');
        let htmlContent = '';
        infoLines.forEach(line => {
            htmlContent += `<p>${line}</p>`;
        });

        $tooltip.html(htmlContent);

        // Se usa .offset() para obtener la posicion exacta
        const inputOffset = $(this).offset();
        const inputHeight = $(this).outerHeight(); // Altura del input, incluyendo padding y border
        
        // Posicionar el tooltip
        $tooltip.css({
            // Calcular la posición TOP: top del input + altura del input + un pequeño margen (5px)
            top: inputOffset.top + inputHeight + 5, 
            
            // Calcular la posición LEFT: alinear con el lado izquierdo del input
            left: inputOffset.left, 
            
            opacity: 1
        }).removeClass('hidden');

    });

    // Función para ocultar el tooltip (sin cambios)
    $('input[data-info], textarea[data-info]').on('mouseleave', function() {
        $tooltip.addClass('hidden');
    });

});