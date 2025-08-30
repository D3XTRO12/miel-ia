# Dockerfile optimizado para SQLite únicamente
FROM python:3.11-slim

#ENV
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app \
    DATABASE_URI=sqlite:///./test.db

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/
COPY trained_models/ ./trained_models/
COPY test.db ./test.db
COPY alembic/ ./alembic/
COPY alembic.ini ./alembic.ini
COPY start.sh ./start.sh
COPY .env* ./

RUN adduser --disabled-password --gecos '' appuser \
    && chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]