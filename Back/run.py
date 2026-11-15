import os
import sys
import uvicorn
from dotenv import load_dotenv

# Consolas Windows (cp1252) no pueden imprimir emoji sin esto
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

load_dotenv()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    print(f"🚀 Servidor corriendo en http://localhost:{port}")
    print(f"🚀 SWAGGER http://localhost:{port}/docs")
    # reload_dirs=["app"] hace que solo vigile tus archivos de código y no .venv
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        reload_dirs=["app"],
    )
