from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from app.routers import crops, rotations, regions

openapi_tags = [
    {
        "name": "Regiones",
        "description": "Gestión de las 3 regiones de San Luis (**norte**, **centro**, **sur**), delimitador provincial (mínimo 50% en San Luis) y Usuarios con su array de Tierras.",
    },
    {
        "name": "Estrategias",
        "description": "Motor inteligente de estrategias de rotación de cultivos calibrado por región de San Luis y prioridades del productor.",
    },
    {
        "name": "Crops",
        "description": "Catálogo de cultivos regionales disponibles en San Luis con sus rasgos hídricos y edáficos.",
    },
]

app = FastAPI(
    title="Adapting Farms with NASA Data API - San Luis",
    description="API de apoyo a la decisión agrícola por regiones de San Luis (Norte, Centro y Sur) con datos satelitales NASA POWER",
    version="0.2.0",
    openapi_tags=openapi_tags,
)

# Middlewares (CORS habilitado para React + Vite)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Redirección automática de la raíz a la documentación interactiva Swagger
@app.get("/", include_in_schema=False)
def root_redirect():
    return RedirectResponse(url="/docs")


# Routers de la API (Controladores)
app.include_router(regions.router)
app.include_router(rotations.router)
app.include_router(crops.router)


# Ruta de prueba / estado del servidor
@app.get("/health", tags=["Salud del Servidor"])
@app.get("/api/health", tags=["Salud del Servidor"])
def health_check():
    return {
        "status": "ok",
        "message": "Servidor de Adapting Farms with NASA Data funcionando correctamente",
    }
