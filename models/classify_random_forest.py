from sklearn.ensemble import RandomForestClassifier

def create_model():
    """
    Random Forest con hiperparámetros ajustados para reducir overfitting.
    """
    return RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        min_samples_split=12,
        min_samples_leaf=5,
        max_features='sqrt',
        class_weight='balanced',
        bootstrap=True,
        random_state=42,
        n_jobs=-1
    )
