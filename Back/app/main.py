from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import crops, rotations, simulation

app = FastAPI(
    title="Adapting Farms with NASA Data API",
    description="API de apoyo a la decisión para adaptación agrícola con datos satelitales NASA POWER",
    version="0.1.0",
)

# Middlewares (CORS habilitado para React + Vite)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "*",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_private_network=True,
)

# Routers de la API
app.include_router(crops.router)
app.include_router(rotations.router)
app.include_router(simulation.router)


# Ruta de prueba / estado del servidor
@app.get("/api/health", tags=["Salud del Servidor"])
def health_check():
    return {
        "status": "ok",
        "message": "Servidor de Adapting Farms with NASA Data funcionando correctamente",
    }
