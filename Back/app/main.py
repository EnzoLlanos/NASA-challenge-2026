from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import crops, rotations

app = FastAPI(
    title="Adapting Farms with NASA Data API",
    version="0.1.0",
)

# Middlewares (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers de la API
app.include_router(crops.router)
app.include_router(rotations.router)


# Ruta de prueba / estado del servidor
@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "message": "Servidor de Adapting Farms with NASA Data funcionando correctamente",
    }

