from analizador_metadatos import extract_metadata

if __name__ == '__main__':
    
    #filepath = r"C:\Users\Héctor\OneDrive\Escritorio\Python en Ciberseguridad Udemy\Analisis de metadatos con Python\analizador_metadatos\Descargas\ejemplo_imagen_metadatos_gps.jpg"
    filepath = r'analizador_metadatos\imagen_prueba.jpg'
    filepath = r'analizador_metadatos\PDF_metadata.pdf'
    metadata = extract_metadata(filepath)
    
    for clave, valor in metadata.items():
        print(f'{clave} : {valor}')
        
    