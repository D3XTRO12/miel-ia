from joblib import load
import pandas as pd

class BinaryPredictor:
    def __init__(self, model_paths: dict):
        self.rf_model = load(model_paths['rf'])
        self.xgb_model = load(model_paths['xgb'])
        self.log_model = load(model_paths['log'])
        print("Modelos de predicción binaria cargados.")

    def predict(self, df: pd.DataFrame) -> dict:
        return {
            "rf": int(self.rf_model.predict(df)[0]),
            "xgb": int(self.xgb_model.predict(df)[0]),
            "log": int(self.log_model.predict(df)[0]),
        }

class MultiClassPredictor:
    def __init__(self, model_paths: dict):
        self.rf_model = load(model_paths['rf'])
        self.xgb_model = load(model_paths['xgb'])
        self.log_model = load(model_paths['log'])
        print("Modelos de predicción multiclase cargados.")

    def predict(self, df: pd.DataFrame) -> dict:
        return {
            "rf": int(self.rf_model.predict(df)[0]),
            "xgb": int(self.xgb_model.predict(df)[0]),
            "log": int(self.log_model.predict(df)[0]),
        }