import os
import uvicorn
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    print(f"Servidor corriendo en http://localhost:{port}")
    print(f"SWAGGER http://localhost:{port}/docs")
    # reload_dirs=["app"] hace que solo vigile tus archivos de código y no .venv
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        reload_dirs=["app"],
    )
