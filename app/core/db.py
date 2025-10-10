from sqlalchemy import Engine, create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import QueuePool
from sqlalchemy import event
from .config import settings
import os
from dotenv import load_dotenv
from pathlib import Path
from urllib.parse import quote_plus

Base = declarative_base()

# Configuración específica para MySQL
engine_kwargs = {
    "poolclass": QueuePool,
    "pool_size": 5,
    "max_overflow": 10,
    "pool_pre_ping": True,
    "pool_recycle": 3600,
    "connect_args": {
        "connect_timeout": 5,
        "charset": "utf8mb4"
    }
}

basedir = os.path.abspath(Path(__file__).parents[2])
load_dotenv(os.path.join(basedir, '.env'))

# Usar directamente la configuración de settings
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# Crear el engine de MySQL
try:
    engine = create_engine(SQLALCHEMY_DATABASE_URL, **engine_kwargs)
    print(f"✅ Motor MySQL creado para: {settings.DB_NAME}@{settings.DB_HOST}")
except Exception as e:
    raise ValueError(f"Error al crear el motor de base de datos MySQL: {e}")

# Configurar sesión
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False
)

def get_db_session():
    """
    Generador de sesiones de base de datos con manejo de errores
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()
        raise
    finally:
        db.close()

def check_database_connection():
    """
    Verifica si la conexión a la base de datos funciona
    """
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("✅ Conexión a MySQL verificada exitosamente")
        return True
    except Exception as e:
        print(f"❌ Error en conexión a MySQL: {e}")
        return False

def create_tables():
    """
    Crear todas las tablas definidas en los modelos
    """
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Tablas de MySQL creadas exitosamente")
    except Exception as e:
        raise ValueError(f"Error al crear las tablas en MySQL: {e}")

def get_database_info():
    """
    Obtiene información de la base de datos MySQL
    """
    try:
        with engine.connect() as conn:
            # Obtener versión de MySQL
            result = conn.execute("SELECT VERSION()")
            version = result.scalar()
            
            # Obtener lista de tablas
            result = conn.execute("SHOW TABLES")
            tables = [row[0] for row in result]
            
            return {
                "version": version,
                "tables": tables,
                "database": settings.DB_NAME,
                "host": settings.DB_HOST
            }
    except Exception as e:
        return {"error": str(e)}
