import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, roc_curve, auc
from sklearn.preprocessing import LabelEncoder, label_binarize
from scikeras.wrappers import KerasClassifier
from tqdm import tqdm
import joblib
from app.infrastructure.ml.classify.classify_logistic_regression import create_model as create_logistic_model
from app.infrastructure.ml.classify.classify_random_forest import create_model as create_rf_model
from app.infrastructure.ml.classify.classify_xgboost import create_model as create_xgb_model

# Crear directorios para modelos entrenados y gráficos
trained_models_dir = os.path.join(os.getcwd(), "trained_models", "classify")
os.makedirs(trained_models_dir, exist_ok=True)

graphs_dir = os.path.join(os.getcwd(), "static", "graphs", "classify")
os.makedirs(graphs_dir, exist_ok=True)

# Cargar datos
file_path = os.path.join(os.getcwd(), 'notebooks', 'split', 'emg_classify_final.csv')
data = pd.read_csv(file_path)

# Codificar gb_score: de 1,2,3 a 0,1,2
le = LabelEncoder()
data['gb_score_encoded'] = le.fit_transform(data['gb_score'])
y_original = data['gb_score']  # para reportes humanos
y = data['gb_score_encoded']   # para entrenamiento

# Preparar X
X = data.drop(columns=['gb_score', 'gb_score_encoded', 'gesture', 'is_synthetic', 'label'])

# Configurar validación cruzada estratificada
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

# Diccionario para almacenar resultados
model_results = {}

# Definir modelos
models = {
    'logistic_regression': KerasClassifier(model=create_logistic_model, epochs=50, batch_size=32, verbose=0),
    'random_forest': create_rf_model(),
    'xgboost': create_xgb_model()
}

# Entrenar y evaluar cada modelo
for model_name, model in models.items():
    print(f"\nEntrenando y evaluando modelo: {model_name}")
    y_true_all, y_pred_all, y_prob_all = [], [], []
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
            y_pred = y_pred.astype(int)

        acc = accuracy_score(y_val, y_pred)
        accuracies.append(acc)

        y_true_all.extend(y_val.tolist())
        y_pred_all.extend(y_pred.tolist())

        if hasattr(model, "predict_proba"):
            y_prob = model.predict_proba(X_val)
            y_prob_all.append(y_prob)

    y_true_all = np.array(y_true_all)
    y_pred_all = np.array(y_pred_all)

    print(f"Accuracy promedio ({model_name}): {np.mean(accuracies):.4f}")
    
    # Reporte de clasificación
    class_report = classification_report(y_true_all, y_pred_all, output_dict=True)
    print(f"Reporte de clasificación ({model_name}):")
    for cls in sorted(class_report.keys()):
        if cls not in ['accuracy', 'macro avg', 'weighted avg']:
            print(f"  Clase {cls}: Precisión={class_report[cls]['precision']:.2f}, "
                  f"Recall={class_report[cls]['recall']:.2f}, "
                  f"F1-score={class_report[cls]['f1-score']:.2f}")
    
    # Matriz de confusión
    cm = confusion_matrix(y_true_all, y_pred_all)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=le.classes_, yticklabels=le.classes_)
    plt.xlabel('Predicho')
    plt.ylabel('Real')
    plt.title(f'Matriz de Confusión - {model_name}')
    plt.savefig(os.path.join(graphs_dir, f'confusion_matrix_cv_{model_name}.png'))
    plt.clf()

    # Visualización de métricas por clase
    plt.figure(figsize=(10, 6))
    class_precision = [class_report[str(i)]['precision'] for i in range(3)]
    class_recall = [class_report[str(i)]['recall'] for i in range(3)]
    class_f1 = [class_report[str(i)]['f1-score'] for i in range(3)]
    
    x = np.arange(3)
    width = 0.25
    plt.bar(x - width, class_precision, width, label='Precisión')
    plt.bar(x, class_recall, width, label='Recall')
    plt.bar(x + width, class_f1, width, label='F1-score')
    plt.xlabel('Clase')
    plt.ylabel('Puntuación')
    plt.title(f'Métricas por clase - {model_name}')
    plt.xticks(x, le.classes_)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(graphs_dir, f'metrics_by_class_{model_name}.png'))
    plt.clf()

    # ROC Curve (solo para modelos tradicionales)
    if model_name in ['random_forest', 'xgboost'] and y_prob_all:
        y_prob_all_concat = np.concatenate(y_prob_all)
        y_true_bin = label_binarize(y_true_all, classes=[0, 1, 2])
        fpr = dict()
        tpr = dict()
        roc_auc = dict()
        for i in range(3):
            fpr[i], tpr[i], _ = roc_curve(y_true_bin[:, i], y_prob_all_concat[:, i])
            roc_auc[i] = auc(fpr[i], tpr[i])
        plt.figure()
        for i in range(3):
            plt.plot(fpr[i], tpr[i], label=f'Clase {le.classes_[i]} (AUC = {roc_auc[i]:.2f})')
        plt.plot([0, 1], [0, 1], 'k--')
        plt.xlabel('Tasa de falsos positivos')
        plt.ylabel('Tasa de verdaderos positivos')
        plt.title(f'Curva ROC - {model_name}')
        plt.legend(loc='lower right')
        plt.tight_layout()
        plt.savefig(os.path.join(graphs_dir, f'roc_curve_{model_name}.png'))
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

# Reentrenar y guardar modelos clásicos
print("\nReentrenando modelos completos para guardar...")

final_rf_model = create_rf_model()
final_rf_model.fit(X, y)
joblib.dump(final_rf_model, os.path.join(trained_models_dir, 'random_forest_model.pkl'))

final_xgb_model = create_xgb_model()
final_xgb_model.fit(X, y)
joblib.dump(final_xgb_model, os.path.join(trained_models_dir, 'xgboost_model.pkl'))

print("Modelos Random Forest y XGBoost guardados exitosamente.")
print("Entrenamiento y evaluación finalizados.")
