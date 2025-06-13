from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import QueuePool, StaticPool, NullPool
from sqlalchemy import event
from .config import settings


# Configuración base del motor
Base = declarative_base()
engine_kwargs = {}

# Configuración específica por motor de base de datos
db_url = settings.DATABASE_URL.lower()

if "sqlite" in db_url:
    # Configuración para SQLite
    engine_kwargs.update({
        "connect_args": {"check_same_thread": False},
        "poolclass": StaticPool  # No necesita pooling para SQLite
    })

elif "mysql" in db_url or "mariadb" in db_url:
    # Configuración para MySQL/MariaDB
    engine_kwargs.update({
        "poolclass": QueuePool,
        "pool_size": 5,
        "max_overflow": 10,
        "pool_pre_ping": True,
        "pool_recycle": 3600,
        "connect_args": {
            "connect_timeout": 5,
            "charset": "utf8mb4"
        }
    })

elif "mssql" in db_url or "sqlserver" in db_url:
    # Configuración para SQL Server
    engine_kwargs.update({
        "poolclass": QueuePool,
        "pool_size": 5,
        "max_overflow": 10,
        "pool_pre_ping": True,
        "connect_args": {
            "driver": "ODBC Driver 18 for SQL Server",
            "TrustServerCertificate": "yes",
            "Encrypt": "yes",
            "connection_timeout": 5
        }
    })

else:
    raise ValueError(f"Database URL no soportada: {settings.DATABASE_URL}")

# Crear motor de base de datos
try:
    engine = create_engine(settings.DATABASE_URL, **engine_kwargs)
except Exception as e:
    raise ValueError(f"Error al crear el motor de base de datos: {e}")

# Configurar SessionLocal
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False
)


# Función para obtener sesión de base de datos
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

# Función para verificar conexión
def check_database_connection():
    """
    Verifica si la conexión a la base de datos funciona
    """
    try:
        with engine.connect() as conn:
            if "sqlite" in db_url:
                conn.execute("SELECT 1")
            else:
                conn.execute("SELECT 1")  # Query universal para todos los motores
        return True
    except Exception as e:
        return False

# Función para crear todas las tablas
def create_tables():
    """
    Crear todas las tablas definidas en los modelos
    """
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        raise ValueError(f"Error al crear las tablas: {e}")