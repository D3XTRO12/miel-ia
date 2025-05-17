from xgboost import XGBClassifier

def create_model():
    return XGBClassifier(
        objective='binary:logistic',
        random_state=42,
        n_estimators=100,       # Reduce si es muy alto
        max_depth=3,            # Limita la profundidad de los árboles
        learning_rate=0.05,     # Más bajo → aprendizaje más lento pero más generalizable
        subsample=0.8,          # Muestreo aleatorio de filas
        colsample_bytree=0.8,   # Muestreo aleatorio de columnas por árbol
        reg_alpha=1,            # Regularización L1 (evita complejidad innecesaria)
        reg_lambda=1            # Regularización L2
    )
