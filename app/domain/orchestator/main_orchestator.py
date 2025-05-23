from load_input import load_emg_data
from validate_input import validate_data
from predict_binary import predict_binary_models
from evaluate_binary_votes import should_classify
from predict_classify import predict_classify_models
from aggregate_results import build_output

def run_full_diagnosis_pipeline(csv_path: str):
    df = load_emg_data(csv_path)
    df_valid = validate_data(df)

    binary_predictions = predict_binary_models(df_valid)
    if should_classify(binary_predictions):
        classify_predictions = predict_classify_models(df_valid)
    else:
        classify_predictions = None

    result = build_output(binary_predictions, classify_predictions)
    return result
