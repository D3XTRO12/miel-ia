from fastapi import APIRouter, BackgroundTasks, Depends
import subprocess
import os

from app.infrastructure.db.DTOs.auth_schema import UserOut
from ...api.v1.auth import get_current_user


train_binary= APIRouter()

@train_binary.post("/train-binary")
def train_models(background_tasks: BackgroundTasks, current_user: UserOut = Depends(get_current_user)):
    # Ruta absoluta al script de entrenamiento
    train_script_path = os.path.abspath("train_binary.py")

    # Ruta absoluta al directorio donde se guardarán los modelos
    trained_models_dir = os.path.abspath("trained_models/binary")

    # Asegurarse de que el directorio de modelos entrenados exista
    os.makedirs(trained_models_dir, exist_ok=True)

    # Comando para ejecutar el script de entrenamiento
    command = ["python", train_script_path]

    # Tarea de entrenamiento en segundo plano
    def run_training():
        try:
            result = subprocess.run(command, check=True, capture_output=True)
            print("Entrenamiento completado.")
            print("Salida estándar:", result.stdout.decode())
            print("Errores:", result.stderr.decode())
        except subprocess.CalledProcessError as e:
            print("Error durante el entrenamiento:", e)
            print("Salida estándar:", e.stdout.decode() if e.stdout else "")
            print("Errores:", e.stderr.decode() if e.stderr else "")

    # Agregar la tarea al background
    background_tasks.add_task(run_training)

    return {"message": "Entrenamiento de modelos iniciado en segundo plano."}
