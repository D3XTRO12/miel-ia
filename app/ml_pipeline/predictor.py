import os
from joblib import load
from tensorflow.keras.models import load_model  # Importación añadida
import pandas as pd

class MLPredictor:
    """
    Clase que carga todos los modelos de ML en memoria una sola vez (Singleton)
    y proporciona métodos para realizar predicciones.
    """
    def __init__(self):
        try:
            # Construye la ruta base a la carpeta de modelos desde la ubicación de este archivo
            base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "trained_models"))
            
            # Carga modelos binarios
            self.binary_rf = load(os.path.join(base_path, "binary", "random_forest_model.pkl"))
            self.binary_xgb = load(os.path.join(base_path, "binary", "xgboost_model.pkl"))
            self.binary_log = load_model(os.path.join(base_path, "binary", "logistic_regression_model.keras"))  # Cambiado

            # Carga modelos de clasificación
            self.classify_rf = load(os.path.join(base_path, "classify", "random_forest_model.pkl"))
            self.classify_xgb = load(os.path.join(base_path, "classify", "xgboost_model.pkl"))
            self.classify_log = load_model(os.path.join(base_path, "classify", "logistic_regression_model.keras"))  # Cambiado
            
            print("✅ Modelos de ML cargados en memoria exitosamente.")
        except FileNotFoundError as e:
            print(f"❌ ERROR CRÍTICO: No se pudo encontrar un archivo de modelo. La aplicación no podrá realizar diagnósticos. Detalle: {e}")
            raise
        except Exception as e:
            print(f"❌ ERROR CRÍTICO: Ocurrió un error inesperado al cargar los modelos: {e}")
            raise

    def predict_binary(self, df: pd.DataFrame) -> dict:
        """Realiza predicciones con el ensamblaje de modelos binarios."""
        df_single_row = df.head(1)
        return {
            # LA CORRECCIÓN: .flatten()[0] asegura que obtengamos un escalar
            # sin importar si el output es [1] o [[1]].
            "rf": int(self.binary_rf.predict(df_single_row).flatten()[0]),
            "xgb": int(self.binary_xgb.predict(df_single_row).flatten()[0]),
            "log": int(self.binary_log.predict(df_single_row).flatten()[0]),
        }

    def predict_classify(self, df: pd.DataFrame) -> dict:
        """Realiza predicciones con el ensamblaje de modelos de clasificación."""
        df_single_row = df.head(1)
        return {
            # LA CORRECCIÓN: .flatten()[0] se aplica aquí también.
            "rf": int(self.classify_rf.predict(df_single_row).flatten()[0]),
            "xgb": int(self.classify_xgb.predict(df_single_row).flatten()[0]),
            "log": int(self.classify_log.predict(df_single_row).flatten()[0]),
        }

# --- Instancia Única (Singleton) ---
ml_predictor = MLPredictor()
