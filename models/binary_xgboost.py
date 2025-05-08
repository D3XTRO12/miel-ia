from xgboost import XGBClassifier

def create_model():
    return XGBClassifier(objective='binary:logistic', random_state=42)
