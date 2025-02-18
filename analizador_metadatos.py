from abc import ABC, abstractmethod
from PIL import Image
import mimetypes


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
                    return {Image.ExifTags.TAGS.get(key, key): value
                            for key , value in exif.items() if key in Image.ExifTags.TAGS}
                    
                       
                else: 
                    return {'Error' : 'No se encontraron metadatos EXIF'}
                
            
            elif img.format in ['PNG']:
                
                if img.info:
                    return img.info
                
                else:
                    return {'Error' : 'No se encontraron metadatos'}
                
                
            else:
                return {'Error' : 'Formato de imagen no soportado'}
             
class MetadataExtractorFactory:
    @staticmethod
   
    def get_extractor(filepath):
        
        tipo_de_archivo, _ = mimetypes.guess_type(filepath)
        if tipo_de_archivo:
            if tipo_de_archivo.startswith('image'):
                return ImageMetadataExtractor()
            
    @staticmethod      
    def extract_metadata(filepath):
        extractor = MetadataExtractorFactory.get_extractor(filepath) 
        return extractor.extract(filepath)
              
                
                
extract_metadata = MetadataExtractorFactory.extract_metadata
    