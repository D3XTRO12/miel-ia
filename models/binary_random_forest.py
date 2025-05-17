from sklearn.ensemble import RandomForestClassifier

def create_model():
    return RandomForestClassifier(
        n_estimators=100,         # Podrías reducirlo a 50 si el dataset es pequeño
        max_depth=10,             # Limita la profundidad de los árboles
        min_samples_split=10,     # Mínimo de muestras para dividir un nodo
        min_samples_leaf=4,       # Mínimo de muestras por hoja
        max_features='sqrt',      # Subconjunto de features para cada split
        bootstrap=True,           # Usa bootstrapping (por defecto True)
        random_state=42
    )
