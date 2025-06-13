import os
from typing import List, Optional, Union
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class Settings(BaseSettings):
    # Información de la aplicación
    APP_NAME: str = "API de Clasificación Binaria"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "API para realizar predicciones de clasificación binaria utilizando múltiples modelos de ML"
    
    # Configuración del servidor
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    
    # Base de datos
    DATABASE_URL: str = os.getenv("DATABASE_URI")
    print(f"✅ Usando DATABASE_URI: {DATABASE_URL}")
    
    # CORS - Simplificado sin validators
    ALLOWED_ORIGINS: Union[str, List[str]] = "*"
    ALLOWED_METHODS: Union[str, List[str]] = "*"
    ALLOWED_HEADERS: Union[str, List[str]] = "*"
    ALLOW_CREDENTIALS: bool = True
    
    # Configuración de Uvicorn
    WORKERS: int = 1
    RELOAD: bool = True
    
    # Configuración de logging
    LOG_LEVEL: str = "DEBUG"
    
    # Configuración de ML
    MODELS_PATH: str = "trained_models"
    BINARY_MODELS_PATH: str = "trained_models/binary"
    CLASSIFY_MODELS_PATH: str = "trained_models/classify"
    
    @property
    def is_development(self) -> bool:
        return self.ENVIRONMENT == "development"
    
    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "production"
    
    @property
    def is_testing(self) -> bool:
        return self.ENVIRONMENT == "testing"
    
    @property
    def cors_origins(self) -> List[str]:
        """Convierte ALLOWED_ORIGINS a lista si es necesario"""
        if isinstance(self.ALLOWED_ORIGINS, str):
            if self.ALLOWED_ORIGINS == "*":
                return ["*"]
            return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",") if origin.strip()]
        return self.ALLOWED_ORIGINS
    
    @property
    def cors_methods(self) -> List[str]:
        """Convierte ALLOWED_METHODS a lista si es necesario"""
        if isinstance(self.ALLOWED_METHODS, str):
            if self.ALLOWED_METHODS == "*":
                return ["*"]
            return [method.strip() for method in self.ALLOWED_METHODS.split(",") if method.strip()]
        return self.ALLOWED_METHODS
    
    @property
    def cors_headers(self) -> List[str]:
        """Convierte ALLOWED_HEADERS a lista si es necesario"""
        if isinstance(self.ALLOWED_HEADERS, str):
            if self.ALLOWED_HEADERS == "*":
                return ["*"]
            return [header.strip() for header in self.ALLOWED_HEADERS.split(",") if header.strip()]
        return self.ALLOWED_HEADERS
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": True,
        "extra": "ignore"  # Ignora campos extra del .env
    }

# Instancia única de configuración
try:
    settings = Settings()
    print("✅ Configuración cargada correctamente")
except Exception as e:
    print(f"❌ Error al cargar configuración: {e}")
    # Configuración de emergencia
    settings = Settings(
        ENVIRONMENT="development",
        DEBUG=True,
        DATABASE_URL="sqlite:///./emergency.db",
        ALLOWED_ORIGINS="*",
        ALLOWED_METHODS="*",
        ALLOWED_HEADERS="*"
    )
    print("🚨 Usando configuración de emergencia")