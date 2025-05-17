import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import accuracy_score, roc_curve, auc, confusion_matrix, roc_auc_score
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb
import joblib
from tqdm import tqdm
from scikeras.wrappers import KerasClassifier
from models.binary_logistic_regression import create_model as create_logistic_model
from models.binary_random_forest import create_model as create_rf_model
from models.binary_xgboost import create_model as create_xgb_model

trained_models_dir = os.path.join(os.getcwd(), "trained_models", "binary")
os.makedirs(trained_models_dir, exist_ok=True)

graphs_dir = os.path.join(os.getcwd(), "static", "graphs", "binary")
os.makedirs(graphs_dir, exist_ok=True)

file_path = os.path.join(os.getcwd(), 'analysis', 'split','emg_binary_final.csv')
data = pd.read_csv(file_path)

print(f"Valores únicos en gb_score: {data['gb_score'].unique()}")
print(f"Tipo de gb_score: {data['gb_score'].dtype}")

if len(data['gb_score'].unique()) > 2:
    print("Advertencia: gb_score contiene más de 2 clases, forzando binarización")
    data['gb_score'] = (data['gb_score'] > 0).astype(int)
    print(f"Después de binarización: {data['gb_score'].unique()}")

X = data.drop(columns=['gb_score', 'gesture', 'is_synthetic', 'label'])
y = data['gb_score'].astype(int)

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

model_results = {}

models = {
    'logistic_regression': KerasClassifier(model=create_logistic_model, epochs=50, batch_size=32, verbose=0),
    'random_forest': create_rf_model(),
    'xgboost': create_xgb_model()
}

for model_name, model in models.items():
    print(f"\nEntrenando y evaluando modelo: {model_name}")
    y_true_all, y_pred_all, y_proba_all = [], [], []
    accuracies = []

    if model_name in ['random_forest', 'xgboost']:
        folds = tqdm(skf.split(X, y), desc=f"Validación cruzada - {model_name}", ncols=100)
    else:
        folds = skf.split(X, y)

    for train_index, val_index in folds:
        X_train, X_val = X.iloc[train_index], X.iloc[val_index]
        y_train, y_val = y.iloc[train_index], y.iloc[val_index]

        model.fit(X_train, y_train)

        y_pred = model.predict(X_val)
        y_pred = np.array(y_pred)

        if y_pred.ndim > 1 and y_pred.shape[1] > 1:
            y_pred = np.argmax(y_pred, axis=1)
        else:
            y_pred = (y_pred > 0.5).astype(int)

        try:
            y_proba = model.predict_proba(X_val)
            if isinstance(y_proba, list):
                y_proba = np.array(y_proba)
            if y_proba.ndim == 2 and y_proba.shape[1] == 2:
                y_proba = y_proba[:, 1]
            else:
                y_proba = y_proba.ravel()
        except Exception as e:
            print(f"Advertencia: predict_proba no disponible: {e}")
            y_proba = y_pred.astype(float)

        acc = accuracy_score(y_val, y_pred)
        accuracies.append(acc)

        y_true_all.extend(y_val.tolist())
        y_pred_all.extend(y_pred.tolist())
        y_proba_all.extend(y_proba.tolist())

    y_true_all = np.array(y_true_all, dtype=int)
    y_pred_all = np.array(y_pred_all, dtype=int)
    y_proba_all = np.array(y_proba_all, dtype=float)

    print(f"Accuracy promedio ({model_name}): {np.mean(accuracies):.4f}")

    try:
        fpr, tpr, _ = roc_curve(y_true_all, y_proba_all)
        roc_auc = roc_auc_score(y_true_all, y_proba_all)
    except ValueError as e:
        print(f"Error al calcular ROC: {e}")
        y_true_bin = (y_true_all > 0).astype(int)
        fpr, tpr, _ = roc_curve(y_true_bin, y_proba_all)
        roc_auc = roc_auc_score(y_true_bin, y_proba_all)

    plt.figure()
    plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc:.2f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title(f'Curva ROC - {model_name.replace("_", " ").title()} (Cross-Validation)')
    plt.legend(loc="lower right")
    plt.savefig(os.path.join(graphs_dir, f'roc_cv_{model_name}.png'))
    plt.clf()

    cm = confusion_matrix(y_true_all, y_pred_all)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=[0, 1], yticklabels=[0, 1])
    plt.xlabel('Predicho')
    plt.ylabel('Real')
    plt.title(f'Matriz de Confusión - {model_name.replace("_", " ").title()} (Cross-Validation)')
    plt.savefig(os.path.join(graphs_dir, f'confusion_matrix_cv_{model_name}.png'))
    plt.clf()

    model_results[model_name] = model

print("\nGuardando modelos entrenados...")

try:
    if 'logistic_regression' in model_results:
        final_model = model_results['logistic_regression']
        if hasattr(final_model, 'model_'):
            keras_model = final_model.model_
            keras_model.save(os.path.join(trained_models_dir, 'logistic_regression_model.keras'))
            print("Modelo de regresión logística guardado exitosamente.")
except Exception as e:
    print(f"Error al guardar modelo keras: {e}")
    try:
        joblib.dump(final_model, os.path.join(trained_models_dir, 'logistic_regression_model.pkl'))
        print("Modelo de regresión logística guardado como .pkl.")
    except Exception as e2:
        print(f"No se pudo guardar: {e2}")

# Modificación aplicada: reentrenamiento completo antes de guardar modelos RF y XGB
print("\nReentrenando modelos en el dataset completo para guardar...")

final_rf_model = create_rf_model()
final_rf_model.fit(X, y)
joblib.dump(final_rf_model, os.path.join(trained_models_dir, 'random_forest_model.pkl'))

final_xgb_model = create_xgb_model()
final_xgb_model.fit(X, y)
joblib.dump(final_xgb_model, os.path.join(trained_models_dir, 'xgboost_model.pkl'))

print("Modelos Random Forest y XGBoost guardados exitosamente tras reentrenamiento.")
print("Entrenamiento y evaluación completados.")
