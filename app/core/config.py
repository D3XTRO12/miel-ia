import os
import time
from typing import List, Optional, Union
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from sqlalchemy import text

# Cargar variables de entorno
load_dotenv()

class Settings(BaseSettings):
    # Información de la aplicación
    APP: str = "Miel-IA: AI POWERED DIAGNOSIS SYSTEM"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "Miel-IA es un sistema de diagnóstico médico impulsado por IA, diseñado para ayudar a los profesionales de la salud a tomar decisiones informadas y precisas."
    
    # Configuración del servidor
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    
    # Base de datos con fallback automático
    DATABASE_URL: str = None
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.DATABASE_URL = self._get_database_url()
    
    def _get_database_url(self) -> str:
        """
        Determina la URL de la base de datos con fallback automático
        """
        # 1. Intentar Azure SQL Server desde variables de entorno
        azure_url = os.getenv("DATABASE_URL")
        if azure_url and not azure_url.startswith("sqlite"):
            if self._test_connection(azure_url):
                print(f"✅ Usando Azure SQL Server: {azure_url[:50]}...")
                return azure_url
            else:
                print("❌ Azure SQL Server no disponible, usando fallback...")
        
        # 2. Fallback a SQLite local
        sqlite_url = "sqlite:///./test.db"
        print(f"📊 Usando SQLite local: {sqlite_url}")
        return sqlite_url
    
    def _test_connection(self, url: str, timeout: int = 5) -> bool:
        """
        Prueba rápida de conexión a base de datos
        """
        try:
            from sqlalchemy import create_engine
            
            # Configurar argumentos de conexión según el tipo de DB
            connect_args = {"connection_timeout": timeout}
            if "sqlite" in url.lower():
                connect_args = {"check_same_thread": False}
            elif "mssql" in url.lower() or "sqlserver" in url.lower():
                connect_args = {
                    "driver": "ODBC Driver 18 for SQL Server",
                    "TrustServerCertificate": "yes",
                    "Encrypt": "yes",
                    "connection_timeout": timeout
                }
            
            engine = create_engine(url, connect_args=connect_args)
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return True
        except Exception as e:
            print(f"⚠️  Error de conexión: {e}")
            return False
    
    # Configuración de autenticación JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # CORS - Simplificado
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
        "extra": "ignore"
    }

# Instancia única de configuración
try:
    settings = Settings()
    print("✅ Configuración cargada correctamente")
    print(f"🌍 Entorno: {settings.ENVIRONMENT}")
    print(f"📦 Base de datos: {settings.DATABASE_URL[:50]}...")
    print(f"🌐 CORS Orígenes: {settings.cors_origins}")
    print(f"🔧 Modo Debug: {settings.DEBUG}")
    print(f"🔑 Token expira en: {settings.ACCESS_TOKEN_EXPIRE_MINUTES} minutos")
except Exception as e:
    print(f"❌ Error al cargar configuración: {e}")
    # Configuración de emergencia
    settings = Settings(
        ENVIRONMENT="development",
        DEBUG=True,
        ALLOWED_ORIGINS="*",
        ALLOWED_METHODS="*",
        ALLOWED_HEADERS="*",
        ACCESS_TOKEN_EXPIRE_MINUTES=30
    )
    settings.DATABASE_URL = "sqlite:///./emergency.db"
    print("🚨 Usando configuración de emergencia")