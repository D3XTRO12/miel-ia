# app/ml_pipeline/helpers.py
import pandas as pd
from typing import Dict, Any

# Lista de todas las columnas de características que tus modelos esperan.
FEATURE_COLUMNS = [
    'standard_deviation_e1', 'standard_deviation_e2', 'standard_deviation_e3', 'standard_deviation_e4',
    'standard_deviation_e5', 'standard_deviation_e6', 'standard_deviation_e7', 'standard_deviation_e8',
    'root_mean_square_e1', 'root_mean_square_e2', 'root_mean_square_e3', 'root_mean_square_e4',
    'root_mean_square_e5', 'root_mean_square_e6', 'root_mean_square_e7', 'root_mean_square_e8',
    'minimum_e1', 'minimum_e2', 'minimum_e3', 'minimum_e4', 'minimum_e5', 'minimum_e6', 'minimum_e7', 'minimum_e8',
    'maximum_e1', 'maximum_e2', 'maximum_e3', 'maximum_e4', 'maximum_e5', 'maximum_e6', 'maximum_e7', 'maximum_e8',
    'zero_crossings_e1', 'zero_crossings_e2', 'zero_crossings_e3', 'zero_crossings_e4',
    'zero_crossings_e5', 'zero_crossings_e6', 'zero_crossings_e7', 'zero_crossings_e8',
    'average_amplitude_change_e1', 'average_amplitude_change_e2', 'average_amplitude_change_e3',
    'average_amplitude_change_e4', 'average_amplitude_change_e5', 'average_amplitude_change_e6',
    'average_amplitude_change_e7', 'average_amplitude_change_e8',
    'amplitude_first_burst_e1', 'amplitude_first_burst_e2', 'amplitude_first_burst_e3',
    'amplitude_first_burst_e4', 'amplitude_first_burst_e5', 'amplitude_first_burst_e6',
    'amplitude_first_burst_e7', 'amplitude_first_burst_e8',
    'mean_absolute_value_e1', 'mean_absolute_value_e2', 'mean_absolute_value_e3', 'mean_absolute_value_e4',
    'mean_absolute_value_e5', 'mean_absolute_value_e6', 'mean_absolute_value_e7', 'mean_absolute_value_e8',
    'wave_form_length_e1', 'wave_form_length_e2', 'wave_form_length_e3', 'wave_form_length_e4',
    'wave_form_length_e5', 'wave_form_length_e6', 'wave_form_length_e7', 'wave_form_length_e8',
    'willison_amplitude_e1', 'willison_amplitude_e2', 'willison_amplitude_e3', 'willison_amplitude_e4',
    'willison_amplitude_e5', 'willison_amplitude_e6', 'willison_amplitude_e7', 'willison_amplitude_e8'
]


def validate_data(df: pd.DataFrame) -> pd.DataFrame:
    """Valida que el DataFrame contenga las columnas necesarias."""
    missing_cols = [col for col in FEATURE_COLUMNS if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required feature columns in CSV: {', '.join(missing_cols)}")
    return df[FEATURE_COLUMNS]


def should_classify(binary_preds: Dict[str, Any]) -> bool:
    """
    Devuelve True si 2 o más modelos binarios votaron '1' (positivo).
    CORREGIDO: Maneja el formato actual con nested dictionary.
    """
    print(f"🔍 [DEBUG] Evaluando binary_preds: {binary_preds}")

    # Manejar el formato actual que tiene 'predictions' anidado
    if isinstance(binary_preds, dict) and 'predictions' in binary_preds:
        predictions = binary_preds['predictions']
        print(f"🔍 [DEBUG] Predicciones extraídas: {predictions}")
    else:
        # Formato antiguo simple
        predictions = binary_preds
        print(f"🔍 [DEBUG] Usando formato simple: {predictions}")

    # Contar votos positivos
    positive_votes = 0
    for model_name, prediction in predictions.items():
        if prediction == 1:
            positive_votes += 1
            print(f"✅ [DEBUG] {model_name}: POSITIVO")
        else:
            print(f"❌ [DEBUG] {model_name}: NEGATIVO")

    result = positive_votes >= 2
    print(f"📊 [DEBUG] Votos positivos: {positive_votes}/3 -> Resultado: {'POSITIVO' if result else 'NEGATIVO'}")

    return result


def build_final_verdict(
        binary_preds: Dict[str, Any],
        classify_preds: Dict[str, Any] | None,
        binary_explanations: list = None,
        classify_explanations: list = None,
        summary_insights: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Construye el objeto de resultado final con explicabilidad completa.
    CORREGIDO: Usa should_classify correctamente.

    Args:
        binary_preds: Predicciones de modelos binarios (puede ser formato nested)
        classify_preds: Predicciones de modelos de clasificación
        binary_explanations: Explicaciones SHAP para modelos binarios
        classify_explanations: Explicaciones SHAP para modelos de clasificación
        summary_insights: Resumen de insights cruzados
    """
    print(f"🔍 [DEBUG] build_final_verdict recibió binary_preds: {binary_preds}")

    # CORRECCIÓN CRÍTICA: Usar should_classify para determinar si es positivo
    is_positive = should_classify(binary_preds)
    print(f"🎯 [DEBUG] Resultado de should_classify: {is_positive}")

    binary_interpretation = "Positivo para EMG" if is_positive else "Negativo para EMG"
    print(f"📋 [DEBUG] Interpretación binaria final: {binary_interpretation}")

    classification_interpretation = "No aplica (Resultado binario fue negativo)"
    final_class = 0

    if classify_preds and is_positive:  # Solo clasificar si es positivo
        # Manejar formato nested si existe
        if isinstance(classify_preds, dict) and 'predictions' in classify_preds:
            predictions = classify_preds['predictions']
        else:
            predictions = classify_preds

        if predictions:
            votes = list(predictions.values())
            final_class = max(set(votes), key=votes.count)
            classification_interpretation = f"Clasificado en Nivel {final_class}"
            print(f"📈 [DEBUG] Clasificación final: Nivel {final_class}")

    # Estructura base del resultado - MANTENER EL FORMATO ACTUAL
    result = {
        "final_diagnosis": binary_interpretation,
        "classification_level": final_class,
        "details": {
            "binary_model_votes": binary_preds,  # Mantener formato original
            "classification_details": {
                "was_classified": classify_preds is not None and is_positive,
                "model_votes": classify_preds,
                "final_level_assigned": final_class if classify_preds and is_positive else None
            }
        }
    }

    # Agregar explicabilidad si está disponible
    if binary_explanations or classify_explanations or summary_insights:
        result["explanations"] = {}

        if binary_explanations:
            result["explanations"]["binary_decision_factors"] = binary_explanations

        if classify_explanations:
            result["explanations"]["classification_factors"] = classify_explanations

        if summary_insights:
            result["explanations"]["summary_insights"] = summary_insights

        # Agregar metadatos de explicabilidad
        result["explanations"]["metadata"] = {
            "explanation_method": "SHAP (SHapley Additive exPlanations)",
            "explanation_timestamp": pd.Timestamp.now().isoformat(),
            "models_explained": len(binary_explanations or []) + len(classify_explanations or []),
            "interpretation_notes": {
                "shap_values": "Valores positivos empujan hacia la predicción, negativos la alejan",
                "impact_magnitude": "high > 0.1, moderate 0.05-0.1, low < 0.05",
                "value_status": "normal/above_normal/below_normal comparado con rangos típicos",
                "z_score": "Desviaciones estándar del valor normal (|z| > 2 es significativo)"
            }
        }

    print(f"🎉 [DEBUG] Verdict final construido: diagnosis={binary_interpretation}, level={final_class}")
    return result


def generate_human_readable_summary(final_verdict: Dict[str, Any]) -> str:
    """
    Genera un resumen en texto plano para logging o debugging
    """
    diagnosis = final_verdict["final_diagnosis"]
    level = final_verdict["classification_level"]

    summary = f"Diagnóstico: {diagnosis}"
    if level > 0:
        summary += f" - Nivel {level}"

    if "explanations" in final_verdict and "summary_insights" in final_verdict["explanations"]:
        insights = final_verdict["explanations"]["summary_insights"]
        if "most_influential_features" in insights and insights["most_influential_features"]:
            top_feature = insights["most_influential_features"][0]
            summary += f"\nPrincipal factor: {top_feature['metric']} en {top_feature['electrode']}"
            summary += f" (valor: {top_feature['actual_value']}, estado: {top_feature['status']})"

    return summary