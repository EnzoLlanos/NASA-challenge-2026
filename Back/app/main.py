from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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


# Ruta de prueba / estado del servidor
@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "message": "Servidor de Adapting Farms with NASA Data funcionando correctamente",
    }
