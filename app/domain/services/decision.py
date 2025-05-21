def decision_service(model_outputs, thresholds):
    """
    Servicio de decisión que determina la clase final basada en las salidas de múltiples modelos.
    
    Args:
        model_outputs (dict): Diccionario con las probabilidades de predicción de cada modelo.
            Ejemplo: {"logistic_regression": 0.7, "random_forest": 0.9, "xgboost": 0.6}
        thresholds (dict): Diccionario con los umbrales para cada modelo.
            Ejemplo: {"logistic_regression": 0.5, "random_forest": 0.5, "xgboost": 0.5}
    
    Returns:
        int: Decisión final (0 o 1).
    """
    # Verificar que tenemos resultados para todos los modelos
    required_models = ["logistic_regression", "random_forest", "xgboost"]
    for model in required_models:
        if model not in model_outputs or model not in thresholds:
            raise ValueError(f"Falta el resultado o umbral para el modelo '{model}'")
    
    # Determinar la clase predicha por cada modelo según su umbral
    model_decisions = {}
    
    for model_name, probability in model_outputs.items():
        model_threshold = thresholds.get(model_name, 0.5)  # Usar 0.5 como umbral predeterminado
        model_decisions[model_name] = 1 if probability >= model_threshold else 0
    
    # Implementar la lógica de decisión (votación por mayoría)
    # Si al menos 2 de los 3 modelos predicen la clase positiva, la decisión final es positiva
    positive_votes = sum(model_decisions.values())
    final_decision = 1 if positive_votes >= 2 else 0
    
    # Agregar información de diagnóstico para depuración
    print(f"Probabilidades: {model_outputs}")
    print(f"Decisiones individuales: {model_decisions}")
    print(f"Votos positivos: {positive_votes}")
    print(f"Decisión final: {final_decision}")
    
    return final_decision