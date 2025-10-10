from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# Imports de configuración y base de datos
from .core.config import settings
from .core.db import get_db_session, check_database_connection

# Imports de routers
from .api.routes.test_binary import test_binary
from .api.routes.train_binary import train_binary
from .api.routes.train_classify import train_classify
from .api.routes.test_classify import test_classify
from .api.routes.user import router as user_router
from .api.routes.medical_study import router as medical_study_router
from .api.routes.diagnose import router as diagnose_router
from .api.v1.auth import router as auth_router
from .api.v1.role import router as role_router
from .api.v1.register import router as register_router
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Evento de startup y shutdown de la aplicación
    """

    # Verificar conexión a base de datos con más información
    try:
        db_connected = check_database_connection()
        if db_connected:
            print("✅ Database connection successful")
        else:
            # En desarrollo, podemos continuar sin base de datos
            if settings.is_development:
                print("🔧 Running in development mode without database")
            else:
                print("❌ Database required in production mode")
                raise Exception("Database connection failed")
    except Exception as e:
        print(f"❌ Database connection error: {str(e)}")
        if settings.is_development:
            print("🔧 Continuing in development mode...")
        else:
            raise Exception(f"Database connection failed: {str(e)}")
    
    yield
    
    # Shutdow
# Crear la aplicación FastAPI
app = FastAPI(
    title=settings.APP,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan
)

# Configurar CORS usando las propiedades
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.ALLOW_CREDENTIALS,
    allow_methods=settings.cors_methods,
    allow_headers=settings.cors_headers,
)

# Incluir los routers
app.include_router(test_binary, tags=["Test"])
app.include_router(test_classify, tags=["Test"])
app.include_router(train_binary, tags=["Train"])
app.include_router(train_classify, tags=["Train"])
app.include_router(user_router)
app.include_router(medical_study_router)
app.include_router(diagnose_router)
app.include_router(auth_router)
app.include_router(role_router)
app.include_router(register_router)


@app.get("/", tags=["Root"])
async def root():
    return {
        "message": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "status": "running",
        "endpoints": {
            "docs": "/docs",
            "redoc": "/redoc",
            "health": "/health"
        }
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """
    Endpoint de health check para monitoreo
    """
    db_status = check_database_connection()
    
    return {
        "status": "healthy" if db_status else "unhealthy",
        "database": "connected" if db_status else "disconnected",
        "environment": settings.ENVIRONMENT,
        "version": settings.APP_VERSION
    }

# Dependency para obtener sesión de base de datos
def get_db():
    """
    Dependency para inyectar sesión de base de datos
    """
    return get_db_session()

# Para desarrollo local
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=False,  # ❌ Deshabilitar reload para evitar ciclos
        workers=1,
        log_level=settings.LOG_LEVEL.lower()
    )