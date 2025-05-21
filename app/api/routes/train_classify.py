from fastapi import APIRouter, BackgroundTasks
import subprocess
import os

train_classify = APIRouter()

@train_classify.post("/train-classify")
def train_classify_models(background_tasks: BackgroundTasks):
    # Ruta absoluta al script de entrenamiento multiclase
    train_script_path = os.path.abspath("train_classify.py")

    # Ruta absoluta al directorio donde se guardarán los modelos
    trained_models_dir = os.path.abspath("trained_models")

    # Asegurarse de que el directorio de modelos entrenados exista
    os.makedirs(trained_models_dir, exist_ok=True)

    # Comando para ejecutar el script de entrenamiento
    command = ["python", train_script_path]

    # Tarea de entrenamiento en segundo plano
    def run_training():
        try:
            result = subprocess.run(command, check=True, capture_output=True)
            print("Entrenamiento multiclase completado.")
            print("Salida estándar:", result.stdout.decode())
            print("Errores:", result.stderr.decode())
        except subprocess.CalledProcessError as e:
            print("Error durante el entrenamiento multiclase:", e)
            print("Salida estándar:", e.stdout.decode() if e.stdout else "")
            print("Errores:", e.stderr.decode() if e.stderr else "")

    # Agregar la tarea al background
    background_tasks.add_task(run_training)

    return {"message": "Entrenamiento multiclase iniciado en segundo plano."}
