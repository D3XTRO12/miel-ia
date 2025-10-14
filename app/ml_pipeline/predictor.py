import os
import numpy as np
from joblib import load
from tensorflow.keras.models import load_model
import pandas as pd

class MLPredictor:
    """
    Clase que carga todos los modelos de ML en memoria una sola vez (Singleton)
    y proporciona métodos para realizar predicciones con probabilidades.
    """
    def __init__(self):
        try:
            base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "trained_models"))
            
            self.binary_rf = load(os.path.join(base_path, "binary", "random_forest_model.pkl"))
            self.binary_xgb = load(os.path.join(base_path, "binary", "xgboost_model.pkl"))
            self.binary_log = load_model(os.path.join(base_path, "binary", "logistic_regression_model.keras"))

            self.classify_rf = load(os.path.join(base_path, "classify", "random_forest_model.pkl"))
            self.classify_xgb = load(os.path.join(base_path, "classify", "xgboost_model.pkl"))
            self.classify_log = load_model(os.path.join(base_path, "classify", "logistic_regression_model.keras"))
            
        except FileNotFoundError as e:
            raise FileNotFoundError(f"File not found - Background task: {e}")
        except Exception as e:
            raise RuntimeError(f"Error loading models - Background task: {e}")

    def _get_binary_probabilities(self, model, df: pd.DataFrame, model_type: str):
        """Obtiene probabilidades para modelos binarios."""
        if model_type == "keras":
            probs = model.predict(df, verbose=0)
            return probs.flatten()
        else:
            if hasattr(model, 'predict_proba'):
                probs = model.predict_proba(df)
                return probs[:, 1]
            else:
                return model.predict(df).flatten()

    def _get_multiclass_probabilities(self, model, df: pd.DataFrame, model_type: str):
        """Obtiene probabilidades para modelos multiclase."""
        if model_type == "keras":
            probs = model.predict(df, verbose=0)
            return probs
        else:
            if hasattr(model, 'predict_proba'):
                return model.predict_proba(df)
            else:
                preds = model.predict(df)
                n_classes = 3  
                one_hot = np.zeros((len(preds), n_classes))
                for i, pred in enumerate(preds):
                    one_hot[i, int(pred)] = 1.0
                return one_hot

    def predict_binary(self, df: pd.DataFrame) -> dict:
        """Realiza predicciones con el ensamblaje de modelos binarios."""
        df_single_row = df.head(1)
        
        rf_probs = self._get_binary_probabilities(self.binary_rf, df_single_row, "sklearn")
        xgb_probs = self._get_binary_probabilities(self.binary_xgb, df_single_row, "sklearn")
        keras_probs = self._get_binary_probabilities(self.binary_log, df_single_row, "keras")
        
        rf_pred = int(rf_probs[0] > 0.5)
        xgb_pred = int(xgb_probs[0] > 0.5)
        keras_pred = int(keras_probs[0] > 0.5)
        
        ensemble_confidence = float(np.mean([rf_probs[0], xgb_probs[0], keras_probs[0]]))
        
        return {
            "predictions": {
                "Random_Forest": rf_pred,
                "XGBoost": xgb_pred,
                "TensorFlow_Logistic_Regression": keras_pred,
            },
            "probabilities": {
                "Random_Forest_preds": rf_probs.tolist(),
                "XGBoost_preds": xgb_probs.tolist(),
                "TensorFlow_Logistic_Regression_preds": keras_probs.tolist(),
            },
            "ensemble_confidence": ensemble_confidence
        }

    def predict_classify(self, df: pd.DataFrame) -> dict:
        """Realiza predicciones con el ensamblaje de modelos de clasificación."""
        df_single_row = df.head(1)
        
        rf_probs = self._get_multiclass_probabilities(self.classify_rf, df_single_row, "sklearn")
        xgb_probs = self._get_multiclass_probabilities(self.classify_xgb, df_single_row, "sklearn")
        keras_probs = self._get_multiclass_probabilities(self.classify_log, df_single_row, "keras")
        
        rf_pred = int(np.argmax(rf_probs[0]))
        xgb_pred = int(np.argmax(xgb_probs[0]))
        keras_pred = int(np.argmax(keras_probs[0]))
        
        predictions = [rf_pred, xgb_pred, keras_pred]
        predicted_class = max(set(predictions), key=predictions.count)
        
        rf_conf = rf_probs[0][predicted_class]
        xgb_conf = xgb_probs[0][predicted_class]
        keras_conf = keras_probs[0][predicted_class]
        ensemble_confidence = float(np.mean([rf_conf, xgb_conf, keras_conf]))
        
        return {
            "predictions": {
                "Random_Forest": rf_pred,
                "XGBoost": xgb_pred,
                "TensorFlow_Logistic_Regression": keras_pred,
            },
            "probabilities": {
                "Random_Forest_preds": rf_probs.tolist(),
                "XGBoost_preds": xgb_probs.tolist(),
                "TensorFlow_Logistic_Regression_preds": keras_probs.tolist(),
            },
            "predicted_class": predicted_class,
            "ensemble_confidence": ensemble_confidence
        }

ml_predictor = MLPredictor()