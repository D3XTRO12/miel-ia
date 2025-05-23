from joblib import load

rf_model = load("models/classify/random_forest.joblib")
xgb_model = load("models/classify/xgboost.joblib")
log_model = load("models/classify/logistic.joblib")

def predict_classify_models(df):
    return {
        "rf": int(rf_model.predict(df)[0]),
        "xgb": int(xgb_model.predict(df)[0]),
        "log": int(log_model.predict(df)[0]),
    }
