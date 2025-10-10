#!/bin/bash
# Script para iniciar en producción

# Configurar PYTHONPATH
export PYTHONPATH=/app/app

# Ejecutar migraciones si es necesario (opcional)
# alembic upgrade head

# Iniciar aplicación con múltiples workers
exec uvicorn app.main:app \
    --host 0.0.0.0 \
    --port ${PORT:-8000} \
    --workers ${WORKERS:-4}