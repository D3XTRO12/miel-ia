# from fastapi import FastAPI
from routes.train import router as train_router  # ajusta el path según tu estructura

# app = FastAPI()
# 
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.test import test_router

# Crear la aplicación FastAPI
app = FastAPI(
    title="API de Clasificación Binaria",
    description="API para realizar predicciones de clasificación binaria utilizando múltiples modelos de ML",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica los orígenes permitidos en lugar de "*"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir los routers
app.include_router(test_router, tags=["test"])
app.include_router(train_router, tags=["train"])

@app.get("/")
async def root():
    return {
        "message": "API de Clasificación Binaria",
        "version": "1.0.0",
        "endpoints": [
            {
                "path": "/api/test",
                "method": "POST",
                "description": "Realiza una clasificación binaria utilizando múltiples modelos"
            }
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)