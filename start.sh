#!/bin/bash

echo "🚀 Iniciando Miel-IA..."

# Función para probar conexión a Azure SQL Server
test_azure_connection() {
    echo "🔍 Probando conexión a Azure SQL Server..."
    
    # Intentar conectar usando Python
    python3 -c "
import os
import sys
sys.path.append('/app')
from app.core.config import settings

try:
    if 'sqlite' not in settings.DATABASE_URL.lower():
        from sqlalchemy import create_engine
        engine = create_engine(settings.DATABASE_URL, connect_args={'connection_timeout': 5})
        with engine.connect() as conn:
            conn.execute('SELECT 1')
        print('✅ Conexión a Azure SQL Server exitosa')
        sys.exit(0)
    else:
        print('📝 Usando SQLite desde configuración')
        sys.exit(1)
except Exception as e:
    print(f'❌ Error conectando a Azure SQL Server: {e}')
    sys.exit(1)
"
    return $?
}

# Configurar fallback a SQLite si Azure SQL Server no está disponible
if ! test_azure_connection; then
    echo "🔄 Configurando fallback a SQLite..."
    export DATABASE_URI="sqlite:///./test.db"
    echo "📊 Usando base de datos local: $DATABASE_URI"
fi

# Crear tablas si es necesario
echo "🏗️  Verificando/creando estructura de base de datos..."
python3 -c "
import sys
sys.path.append('/app')
from app.core.db import create_tables, check_database_connection
from app.core.config import settings

print(f'📊 Base de datos configurada: {settings.DATABASE_URL}')

if check_database_connection():
    print('✅ Conexión a base de datos exitosa')
    try:
        create_tables()
        print('🏗️  Estructura de base de datos verificada')
    except Exception as e:
        print(f'⚠️  Error creando tablas: {e}')
else:
    print('❌ No se pudo conectar a la base de datos')
    exit(1)
"

# Iniciar la aplicación
echo "🌟 Iniciando servidor FastAPI..."
if [ "$ENVIRONMENT" = "production" ]; then
    echo "🚀 Modo producción"
    exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
else
    echo "🔧 Modo desarrollo"
    exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
fi