from analizador_metadatos import extract_metadata
import mimetypes



#Forzaando el registro del MIME type para los archivos .docx
mimetypes.add_type('application/vnd.openxmlformats-officedocument.wordprocessingml.document', '.docx')


if __name__ == '__main__':
    
    
    filepath = r'analizador_metadatos\imagen_prueba.jpg'
    filepath = r'analizador_metadatos\PDF_metadata.pdf'
    filepath = r'analizador_metadatos\prueba.docx'
    
    metadata = extract_metadata(filepath)
    
    for clave, valor in metadata.items():
        print(f'{clave} : {valor}')
        
    