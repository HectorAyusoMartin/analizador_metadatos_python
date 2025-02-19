import argparse
import mimetypes
from analizador_metadatos import extract_metadata

# Forzamos el registro del MIME type para los archivos .docx
mimetypes.add_type('application/vnd.openxmlformats-officedocument.wordprocessingml.document', '.docx')

def mostrar_bienvenida():
    print(f'Creado por: Héctor Ayuso')
    print('\n')
    print('\n')
    print("================================================")
    print("¡Bienvenido a la App de Extracción de Metadatos!")
    print("================================================")
    print('\n')
    print("Usa el comando 'extraer' para extraer metadatos ")
    print("de un archivo.")
    print("Este script ha sido desarrolado en Python, y")
    print("es capaz de extraer metadatos de imágenes, PDFs")
    print("y archivos DOCX.")
    print("Los metadatos extraídos dependerán del tipo de")
    print("archivo que se analice.")
    print("Este script cuenta con la funcionalidad añadida")
    print("de encontrar correos electroónicos dentro de")
    print("los PDF analizados y extarerlos en una [lista].")
    print("Este script ha sido desarrollado con fines de ")
    print("aprendizaje y no debe ser utilizado para")
    print("propósitos maliciosos.")
    print('\n')
    print("Ejemplo de uso:")
    print('\n')
    print("-----------------------------------------------\n")
    print("python cli.py extraer --file imagen_prueba.jpg")
    print('\n')
    print("-----------------------------------------------\n")

def extraer_metadatos(args):
    filepath = args.file
    print(f"\n[+] Analizando el archivo: {filepath}")
    print('\n')
    print('\n')
    try:
        metadata = extract_metadata(filepath)
        print("\n=== Metadatos extraídos ===")
        print('\n')
        
        for clave, valor in metadata.items():
            print(f"{clave} : {valor}")
         
        print("\n===========================")   
        
    except Exception as e:
        print("\n¡Ups! Se produjo un error al extraer los metadatos:")
        print(e)

def main():
    mostrar_bienvenida()
    
    parser = argparse.ArgumentParser(
        description="Interfaz de línea de comandos para extraer metadatos."
    )
    
    subparsers = parser.add_subparsers(title="Comandos", dest="comando")
    
    
    # Comando: extraer
    parser_extraer = subparsers.add_parser("extraer", help="Extrae metadatos de un archivo")
    parser_extraer.add_argument(
        "--file", "-f",
        type=str,
        required=True,
        help="Ruta del archivo a analizar (soporta imágenes, PDFs y DOCX)"
    )
    parser_extraer.set_defaults(func=extraer_metadatos)
    
    args = parser.parse_args()
    
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
