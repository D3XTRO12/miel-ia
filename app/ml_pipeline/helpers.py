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

def should_classify(binary_preds: Dict[str, int]) -> bool:
    """Devuelve True si 2 o más modelos binarios votaron '1' (positivo)."""
    positives = sum(vote for vote in binary_preds.values() if vote == 1)
    return positives >= 2

def build_final_verdict(binary_preds: Dict[str, int], classify_preds: Dict[str, int] | None) -> Dict[str, Any]:
    """Construye el objeto de resultado final con una interpretación clara."""
    is_positive = should_classify(binary_preds)
    binary_interpretation = "Positivo para EMG" if is_positive else "Negativo para EMG"

    classification_interpretation = "No aplica (Resultado binario fue negativo)"
    final_class = 0
    
    if classify_preds:
        votes = list(classify_preds.values())
        final_class = max(set(votes), key=votes.count)
        classification_interpretation = f"Clasificado en Nivel {final_class}"

    return {
        "final_diagnosis": binary_interpretation,
        "classification_level": final_class,
        "details": {
            "binary_model_votes": binary_preds,
            "classification_details": {
                "was_classified": classify_preds is not None,
                "model_votes": classify_preds,
                "final_level_assigned": final_class if classify_preds else None
            }
        }
    }
