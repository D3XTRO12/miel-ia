# Usar imagen base optimizada de Python
FROM python:3.11-slim

# Variables de entorno para optimización
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONPATH=/app/app

# Instalar dependencias del sistema necesarias para SQL Server y compilación
RUN apt-get update \
 && apt-get install -y gnupg2 curl \
 && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
 && curl https://packages.microsoft.com/config/debian/11/prod.list \
    > /etc/apt/sources.list.d/mssql-release.list \
 && apt-get update \
 && apt-get remove -y libodbc2 libodbcinst2 odbcinst unixodbc-common \
 && ACCEPT_EULA=Y apt-get install -y msodbcsql18


# Instalar Microsoft ODBC Driver para SQL Server
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18 \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar requirements primero (para aprovechar cache de Docker)
COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY . .

# Crear usuario no-root por seguridad
RUN adduser --disabled-password --gecos '' appuser \
    && chown -R appuser:appuser /app
USER appuser

# Exponer puerto
EXPOSE 8000

# Comando optimizado para producción con Uvicorn
# Apunta a app/main.py en lugar de main.py
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]