El desarrollo de este Proyecto ha sido planteado con el concepto de 'Factory'
Factory es un patrón de diseño, que nos permite crear Clases o programas que 
despues puedan extenderse facilmente con módulos adicionales.
Esto será un motor que extraiga metadatados de distintos tipos de archivos.

También se aplicará en este Proyecto el concepto y funcionalidad de las clases Abstractas
y métodos Estáticos. El objetivc es estructurar el Script con conceptos POO en Python.

La imagen de prueba JPG se obtuvo de un repositorio Github especializado en imagenes EXIF, de 
distintas clases.
El repositorio es: https://github.com/ianare/exif-samples

===Como Usar===

Abrir main.py, y cambiar el valor de la variable 'filepath' por la ruta del archivo +
nombre del archivo a extraer los metadatos.

Main.py llamará a analizador_metadatos.py, y dependiendo del mime type del archivo a analizar, 
llamará a la funcion correspondiente, que devolvera un tipo de extractor especial para tratar
correctamente la extracción de los metadatos dependiendo del tipo de archivo.

Los resultados de la extracción serán mostrados por consola, sin demasiado procesamiento de datos
final.




