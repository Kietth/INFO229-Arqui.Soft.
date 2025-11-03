from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, date

# --- 1. Definición del Modelo de Datos (Pydantic) ---

class Noticia(BaseModel):
    """Modelo de datos para una noticia individual."""
    id: str 
    fecha_publicacion: datetime
    fuente: str 
    titulo: str
    contenido: str
    tema: Optional[str] = None

    class Config:
        from_attributes = True

# --- 2. Datos de Prueba (Simulación de la DB/Elasticsearch) ---

DB_SIMULADA: List[Noticia] = [
    Noticia(
        id="N001",
        fecha_publicacion=datetime(2025, 10, 25, 10, 30),
        fuente="El Mercurio",
        titulo="El avance de la IA revoluciona la industria local",
        contenido="Expertos debaten sobre el impacto de la Inteligencia Artificial en el mercado laboral.",
        tema="Tecnología"
    ),
    Noticia(
        id="N002",
        fecha_publicacion=datetime(2025, 10, 24, 15, 0),
        fuente="La Nación",
        titulo="Crisis climática: Sequía afecta a la agricultura del sur",
        contenido="Los agricultores piden ayuda al gobierno tras meses sin lluvia.",
        tema="Medio Ambiente"
    ),
    Noticia(
        id="N003",
        fecha_publicacion=datetime(2025, 10, 25, 11, 45),
        fuente="El Mercurio",
        titulo="Resultados electorales del fin de semana",
        contenido="Análisis detallado de los votos en las principales regiones del país.",
        tema="Política"
    ),
    Noticia(
        id="N004",
        fecha_publicacion=datetime(2025, 10, 20, 8, 0),
        fuente="Diario Financiero",
        titulo="Grandes inversiones en infraestructura tecnológica",
        contenido="Se anuncia un nuevo centro de datos con tecnología de punta.",
        tema="Tecnología"
    ),
]

# --- 3. Inicialización de la API ---

app = FastAPI(
    title="API de Noticias de Prensa (T2 - Beta)",
    description="API para aplicar filtros y búsquedas por palabras clave sobre noticias.",
    version="1.0-beta"
)


# --- 4. Lógica de Filtrado y Búsqueda (Simulada) ---

@app.get("/api/v1/noticias", response_model=List[Noticia])
def listar_noticias_con_filtros(
    # Búsqueda por Palabras Clave
    q: Optional[str] = Query(None, description="Palabra clave a buscar en título y contenido."),
    # Filtro por Medio
    medio: Optional[str] = Query(None, description="Filtrar por el nombre exacto del medio de comunicación."),
    # Filtro por Rango de Fechas
    fecha_inicio: Optional[date] = Query(None, description="Fecha de inicio (YYYY-MM-DD)."),
    fecha_fin: Optional[date] = Query(None, description="Fecha de fin (YYYY-MM-DD)."),
    # Filtro por Tema
    tema: Optional[str] = Query(None, description="Filtrar por el tema (ej: Tecnología, Política).")
):
    """
    Permite buscar noticias por palabras clave y filtrar por múltiples criterios.
    Esta versión beta utiliza la lista de datos simulada (DB_SIMULADA).
    """
    
    resultados = DB_SIMULADA[:]  # Copia la lista para no modificar la original

    # Aplicar Filtro de Palabras Clave (q)
    if q:
        q_lower = q.lower()
        resultados = [
            n for n in resultados 
            if q_lower in n.titulo.lower() or q_lower in n.contenido.lower()
        ]

    # Aplicar Filtro por Medio
    if medio:
        medio_lower = medio.lower()
        resultados = [
            n for n in resultados 
            if n.fuente.lower() == medio_lower
        ]

    # Aplicar Filtro por Tema
    if tema:
        tema_lower = tema.lower()
        resultados = [
            n for n in resultados 
            if n.tema and n.tema.lower() == tema_lower
        ]
    
    # Aplicar Filtro por Rango de Fechas
    if fecha_inicio:
        resultados = [
            n for n in resultados 
            if n.fecha_publicacion.date() >= fecha_inicio
        ]
    if fecha_fin:
        resultados = [
            n for n in resultados 
            if n.fecha_publicacion.date() <= fecha_fin
        ]

    return resultados

# Endpoint para obtener una noticia por ID
@app.get("/api/v1/noticias/{noticia_id}", response_model=Noticia)
def obtener_noticia(noticia_id: str):
    """
    Obtiene una noticia específica usando su ID único.
    """
    noticia = next((n for n in DB_SIMULADA if n.id == noticia_id), None)
    if noticia is None:
        # Lanza un error 404 si la noticia no existe
        raise HTTPException(status_code=404, detail="Noticia no encontrada")
    return noticia

# --- 5. Ejecución ---

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
