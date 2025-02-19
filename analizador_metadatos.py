from abc import ABC, abstractmethod
from PIL import Image , ExifTags
import mimetypes
from pdfminer.high_level import extract_text
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
import re
import docx

def convert_to_degrees(value):
    """Convierte un valor de coordenadas en grados, minutos y segundos a grados decimales"""
    grados , minutos , segundos = value
    return grados + minutos / 60.0 + segundos /3600.0


class MetadataExtractor(ABC):
    @abstractmethod
    def extract(self, filepath):
        pass
    
class ImageMetadataExtractor(MetadataExtractor):
    
    def extract(self, filepath):
        
        
        with Image.open(filepath) as img:
            
            if img.format in ['JPG','JPEG']:
                
                exif = img._getexif()
                
                if exif:
                    #Convertimos las keys a nombres legibles
                    metadata = {ExifTags.TAGS.get(key, key): value
                                for key, value in exif.items() if key in ExifTags.TAGS}
                    
                    #Si no hay informacion GPS, exatremos y convertimos las coordenadas
                    gps_info = metadata.get('GPSInfo')
                    
                    if gps_info:
                        #Obtenemos la información necesaria del GPS
                        lat_ref = gps_info.get(1)
                        lat_tuple = gps_info.get(2)
                        lon_ref = gps_info.get(3)
                        lon_tuple = gps_info.get(4)
                        
                        if lat_ref and lat_tuple and lon_ref and lon_tuple:
                            
                            lat = convert_to_degrees(lat_tuple)
                            lon = convert_to_degrees(lon_tuple)
                            
                            #ajustamos el signo segun la referencia N S E W
                            if lat_ref != 'N':
                                lat = -lat
                            if lon_ref != 'E':
                                lon = -lon
                                
                            #Agregamos las coordenadas al diccionariko de metadatos
                            metadata['Coordenadas'] = f'{lat:.6f}, {lon:.6f}'
                            
                            #Creamos direccion URL para copair y pegar y la agregamos al diccionario metadata
                            metadata['Coordenadas_URL'] = f'https://www.google.com/maps/search/?api=1&query={metadata["Coordenadas"]}'
                            
                    return metadata
                
                else:
                    return {'Error' : 'No se encontraron metadatos EXIF'}
                            
                                
                    
                
            
            elif img.format in ['PNG']:
                
                if img.info:
                    return img.info
                
                else:
                    return {'Error' : 'No se encontraron metadatos'}
                
                
            else:
                return {'Error' : 'Formato de imagen no soportado'}
    
class PdfMetadataExtractor(MetadataExtractor):
    def extract(self, filepath):
        metadata = {}
        with open(filepath, 'rb') as f:
            parser = PDFParser(f)
            doc = PDFDocument(parser)
            if doc.info:
                for info in doc.info:
                    for key, value in info.items():
                        #verificamos si el valor de la clave son bytes
                        if isinstance(value, bytes):
                            try:
                                #Intentaar decodificar en UTF-16BE
                                decoded_value = value.decode('utf-16be')
                            except UnicodeDecodeError:
                                #Intentar decodificarlo en UTF-8
                                decoded_value =  value.decode('utf-8', errors='ignore')
                          
                        else:
                            decoded_value = value
                            
                        metadata[key] = decoded_value
            #Procesamos el texto del PDF para obtener otros datos de interes
            text = extract_text(filepath)
            metadata['Emails'] = self._extract_emails(text)
        return metadata
    
                    
                                 
    def _extract_emails(self, text):
        """Va a utilizar una expresión regular, encontrada en internet, para enccontrar emails en el texto"""
        email_regex = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
        return re.findall(email_regex, text)        

class DocxMetadataExtractor(MetadataExtractor):
    
    def extract(self, filepath):
        doc = docx.Document(filepath)
        prop = doc.core_properties
        attributes = [
            
            "author",   # Autor del documento
            "category", # Categoría del documento 
            "comments", # Comentarios del documento
            "content_status", # Estado del contenido
            "created",  # Fecha de creación
            "identifier", # Identificador
            "keywords", # Palabras clave
            "last_modified_by", # Última persona que modificó el documento
            "last_printed", # Última fecha de impresión
            "language", # Idioma
            "modified", # Fecha de modificación
            "subject", # Asunto
            "title", # Título
            "version" # Versión
        ]
        
        metadata = {attr: getattr(prop, attr, None) for attr in attributes}
        return metadata
     
class MetadataExtractorFactory:
    @staticmethod
   
    def get_extractor(filepath):
        
        tipo_de_archivo, _ = mimetypes.guess_type(filepath)
        
        if tipo_de_archivo:
            if tipo_de_archivo.startswith('image'):
                return ImageMetadataExtractor()
            if tipo_de_archivo == 'application/pdf':
                return PdfMetadataExtractor()
            if tipo_de_archivo == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
                return DocxMetadataExtractor()
            
        raise ValueError('Formato de archivo no soportado')
            
    @staticmethod      
    def extract_metadata(filepath):
        extractor = MetadataExtractorFactory.get_extractor(filepath) 
        return extractor.extract(filepath)
              
                
                
extract_metadata = MetadataExtractorFactory.extract_metadata
    