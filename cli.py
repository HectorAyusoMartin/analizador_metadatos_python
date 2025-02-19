import argparse
import mimetypes
import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.rule import Rule
from analizador_metadatos import extract_metadata

# Forzamos el registro del MIME type para los archivos .docx
mimetypes.add_type('application/vnd.openxmlformats-officedocument.wordprocessingml.document', '.docx')

console = Console()

def mostrar_bienvenida():
    mensaje = (
        "[bold cyan]Creado por: Héctor Ayuso[/bold cyan]\n\n"
        "[bold magenta]¡Bienvenido a la App de Extracción de Metadatos![/bold magenta]\n"
        "\nUsa el comando [green]'extraer'[/green] para extraer metadatos "
        "de un archivo.\n"
        "\nEste script ha sido desarrollado en Python y es capaz de extraer metadatos de imágenes, PDFs y archivos DOCX.\n"
        "También encuentra correos electrónicos en PDFs y los guarda en una [lista].\n"
        "\n[red]¡Importante![/red] No lo uses para fines maliciosos. Este Script se desarrolló con la idea de practicar conocimientos de Ciberseguridad "
        "en Python, y concienciar sobre la privacidad de nuestros activos digitales."
    )
    console.print(Panel(mensaje, title="Bienvenido", border_style="bright_blue"))
    console.print("\nEjemplo de uso:")
    console.print("\n")
    console.print("[yellow]python cli.py extraer --file imagen_prueba.jpg[/yellow]\n")

def extraer_metadatos(args):
    filepath = args.file
    console.print(f"\n[bold green][+] Analizando el archivo: [underline]{filepath}[/underline][/bold green]\n")
    
    try:
        # Forzamos el spinner a mostrarse al menos 2.5 segundos
        with console.status("[bold green]Extrayendo metadatos...[/bold green]", spinner="dots") as status:
            start_time = time.time()
            metadata = extract_metadata(filepath)
            elapsed = time.time() - start_time
            if elapsed < 2.5:
                time.sleep(2.5 - elapsed)
        
        console.print(Rule(style="blue"))
        
        table = Table(title="Metadatos extraídos", show_header=True, header_style="bold blue", show_lines=False)
        table.add_column("Clave", style="dim", width=20)
        table.add_column("Valor", style="red")
        
        items = list(metadata.items())
        for i, (clave, valor) in enumerate(items):
            table.add_row(str(clave), str(valor))
            if i < len(items) - 1:
                table.add_row("", "")
        
        console.print(table)
        console.print(Panel("[bold green]Metadatos extraídos correctamente![/bold green]", border_style="green"))
        
    except Exception as e:
        console.print("\n[bold red]¡Ups! Se produjo un error al extraer los metadatos:[/bold red]")
        console.print(f"[red]{e}[/red]")

def main():
    mostrar_bienvenida()
    
    parser = argparse.ArgumentParser(
        description="Interfaz de línea de comandos para extraer metadatos."
    )
    
    subparsers = parser.add_subparsers(title="Comandos", dest="comando")
    
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
    # Si no se ingresa ningún comando, no se muestra la ayuda y se termina el programa.
    
if __name__ == '__main__':
    main()
