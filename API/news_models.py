# news_model.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class Noticia(BaseModel):
    # Campos almacenados
    id: str # ID único para el documento en la DB/Elasticsearch
    fecha_publicacion: datetime
    fuente: str # Nombre del medio de comunicación
    titulo: str
    contenido: str
    imagenes: List[str] # Lista de URLs de fotografías
    
    # Campos para filtros y clasificaciones
    tema: Optional[str] = None # Para clasificaciones manuales o con IA
    etiquetas_ia: Optional[List[str]] = None # Etiquetas generadas por IA
    
    # Configuración de Pydantic
    class Config:
        from_attributes = True
