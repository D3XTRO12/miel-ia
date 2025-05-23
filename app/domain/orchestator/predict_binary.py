from joblib import load

rf_model = load("models/binary/random_forest.joblib")
xgb_model = load("models/binary/xgboost.joblib")
log_model = load("models/binary/logistic.joblib")

def predict_binary_models(df):
    return {
        "rf": int(rf_model.predict(df)[0]),
        "xgb": int(xgb_model.predict(df)[0]),
        "log": int(log_model.predict(df)[0]),
    }
