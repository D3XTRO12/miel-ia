# app/ml_pipeline/pipeline.py
import pandas as pd
from typing import IO

# Importamos la instancia única de nuestros modelos
from .predictor import ml_predictor

# Importamos nuestras funciones de ayuda actualizadas
from .helpers import validate_data, should_classify, build_final_verdict, generate_human_readable_summary

# Importamos el sistema de explicabilidad
from .explainer import ml_explainer


def run_diagnosis_pipeline(file_stream: IO, include_explanations: bool = True) -> dict:
    """
    Ejecuta el pipeline completo de diagnóstico desde un stream de archivo.
    Ahora incluye explicabilidad usando SHAP.

    Args:
        file_stream: Un objeto tipo archivo (como el de UploadFile.file de FastAPI).
        include_explanations: Si incluir explicaciones SHAP (por defecto True)

    Returns:
        Un diccionario con el veredicto final, detalles del proceso y explicabilidad.
    """
    # 1. Cargar datos desde el stream en memoria y validar su formato
    try:
        df = pd.read_csv(file_stream)
        # La validación selecciona y ordena las columnas, y lanza ValueError si faltan
        df_valid = validate_data(df)
        print(f"✅ Datos validados: {df_valid.shape[0]} filas, {df_valid.shape[1]} características")
    except Exception as e:
        # Captura errores de lectura de CSV o de validación
        raise ValueError(f"Error processing CSV file: {e}")

    # 2. Realizar predicciones usando los modelos en memoria
    print("🤖 Ejecutando predicciones binarias...")
    binary_predictions = ml_predictor.predict_binary(df_valid)
    print(f"📊 Predicciones binarias: {binary_predictions}")

    # 3. Evaluar si se debe proceder a la clasificación
    classify_predictions = None
    if should_classify(binary_predictions):
        print("🎯 Resultado binario positivo - Ejecutando clasificación...")
        classify_predictions = ml_predictor.predict_classify(df_valid)
        print(f"📈 Predicciones de clasificación: {classify_predictions}")
    else:
        print("❌ Resultado binario negativo - No se ejecuta clasificación")

    # 4. Generar explicabilidad si está habilitada
    binary_explanations = None
    classify_explanations = None
    summary_insights = None

    if include_explanations:
        try:
            print("🔍 Generando explicaciones SHAP...")

            # Explicar predicciones binarias
            binary_explanations = ml_explainer.explain_binary_prediction(df_valid, binary_predictions)
            print(f"✅ Explicaciones binarias generadas para {len(binary_explanations)} modelos")

            # Explicar predicciones de clasificación si aplica
            if classify_predictions:
                classify_explanations = ml_explainer.explain_classification_prediction(df_valid, classify_predictions)
                print(f"✅ Explicaciones de clasificación generadas para {len(classify_explanations)} modelos")

            # Generar insights de resumen
            summary_insights = ml_explainer.generate_summary_insights(
                binary_explanations or [],
                classify_explanations or []
            )
            print("✅ Insights de resumen generados")

        except Exception as e:
            print(f"⚠️ Error generando explicaciones (continuando sin ellas): {e}")
            # El sistema continúa funcionando sin explicaciones
            binary_explanations = None
            classify_explanations = None
            summary_insights = None

    # 5. Construir y devolver el resultado final con explicabilidad
    final_verdict = build_final_verdict(
        binary_predictions,
        classify_predictions,
        binary_explanations,
        classify_explanations,
        summary_insights
    )

    # 6. Generar resumen legible para logs
    readable_summary = generate_human_readable_summary(final_verdict)
    print(f"📋 Resumen: {readable_summary}")

    return final_verdict