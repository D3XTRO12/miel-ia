import pandas as pd
from typing import IO

# Importamos la instancia única de nuestros modelos
from .predictor import ml_predictor

# Importamos nuestras funciones de ayuda
from .helpers import validate_data, should_classify, build_final_verdict

def run_diagnosis_pipeline(file_stream: IO) -> dict:
    """
    Ejecuta el pipeline completo de diagnóstico desde un stream de archivo.
    
    Args:
        file_stream: Un objeto tipo archivo (como el de UploadFile.file de FastAPI).

    Returns:
        Un diccionario con el veredicto final y los detalles del proceso.
    """
    # 1. Cargar datos desde el stream en memoria y validar su formato
    try:
        df = pd.read_csv(file_stream)
        # La validación selecciona y ordena las columnas, y lanza ValueError si faltan
        df_valid = validate_data(df)
    except Exception as e:
        # Captura errores de lectura de CSV o de validación
        raise ValueError(f"Error processing CSV file: {e}")

    # 2. Realizar predicciones usando los modelos en memoria
    binary_predictions = ml_predictor.predict_binary(df_valid)
    
    # 3. Evaluar si se debe proceder a la clasificación
    classify_predictions = None
    if should_classify(binary_predictions):
        classify_predictions = ml_predictor.predict_classify(df_valid)

    # 4. Construir y devolver el resultado final
    final_verdict = build_final_verdict(binary_predictions, classify_predictions)
    
    return final_verdict
