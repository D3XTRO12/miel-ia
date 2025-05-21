import asyncio
import numpy as np

async def predict_logistic_regression_async(data, model):
    """
    Realiza una predicción asíncrona utilizando el modelo de regresión logística.
    
    Args:
        data (dict): Datos de entrada para la predicción.
        model: Modelo de regresión logística cargado.
        
    Returns:
        float: Probabilidad predicha para la clase positiva.
    """
    try:
        # Convertir los datos de entrada a un formato adecuado para el modelo
        features = prepare_features(data)
        
        # Ejecutar la predicción en un hilo separado para no bloquear el bucle de eventos
        loop = asyncio.get_event_loop()
        prediction = await loop.run_in_executor(None, lambda: model.predict(features))
        
        # Asegurarse de que la salida sea un valor escalar
        if hasattr(prediction, 'numpy'):
            prediction = prediction.numpy()
        
        if prediction.ndim > 1:
            prediction = prediction.flatten()
        
        # Devolver la probabilidad como un float
        return float(prediction[0])
    
    except Exception as e:
        print(f"Error en la predicción con regresión logística: {e}")
        return 0.0

async def predict_random_forest_async(data, model):
    """
    Realiza una predicción asíncrona utilizando el modelo Random Forest.
    
    Args:
        data (dict): Datos de entrada para la predicción.
        model: Modelo Random Forest cargado.
        
    Returns:
        float: Probabilidad predicha para la clase positiva.
    """
    try:
        # Convertir los datos de entrada a un formato adecuado para el modelo
        features = prepare_features(data)
        
        # Ejecutar la predicción en un hilo separado para no bloquear el bucle de eventos
        loop = asyncio.get_event_loop()
        prediction = await loop.run_in_executor(None, lambda: model.predict_proba(features))
        
        # Obtener la probabilidad de la clase positiva (índice 1)
        return float(prediction[0][1])
    
    except Exception as e:
        print(f"Error en la predicción con Random Forest: {e}")
        return 0.0

async def predict_xgboost_async(data, model):
    """
    Realiza una predicción asíncrona utilizando el modelo XGBoost.
    
    Args:
        data (dict): Datos de entrada para la predicción.
        model: Modelo XGBoost cargado.
        
    Returns:
        float: Probabilidad predicha para la clase positiva.
    """
    try:
        # Convertir los datos de entrada a un formato adecuado para el modelo
        features = prepare_features(data)
        
        # Ejecutar la predicción en un hilo separado para no bloquear el bucle de eventos
        loop = asyncio.get_event_loop()
        prediction = await loop.run_in_executor(None, lambda: model.predict_proba(features))
        
        # Obtener la probabilidad de la clase positiva (índice 1)
        return float(prediction[0][1])
    
    except Exception as e:
        print(f"Error en la predicción con XGBoost: {e}")
        return 0.0

def prepare_features(data):
    """
    Prepara los datos de entrada para la predicción.
    
    Args:
        data (dict): Datos de entrada para la predicción.
        
    Returns:
        numpy.ndarray: Array con las características preparadas.
    """
    # Asumimos que los datos vienen como un diccionario con claves numéricas o como una lista
    if isinstance(data, dict):
        # Si es un diccionario, asumimos que las claves son los índices de las características
        # y los valores son los valores de las características
        if all(isinstance(k, str) and k.isdigit() for k in data.keys()):
            # Convertir claves numéricas a enteros y ordenar
            sorted_items = sorted([(int(k), v) for k, v in data.items()])
            features = np.array([[v for _, v in sorted_items]])
        else:
            # Si las claves no son numéricas, asumimos que son nombres de características
            # y extraemos los valores en algún orden específico
            features = np.array([[data[k] for k in sorted(data.keys())]])
    elif isinstance(data, list):
        # Si es una lista, la convertimos directamente a un array
        features = np.array([data])
    else:
        raise ValueError("Los datos de entrada deben ser un diccionario o una lista")
    
    return features

async def orchestrator_service(data, models):
    """
    Orquesta las predicciones de los modelos de forma asíncrona.
    
    Args:
        data (dict): Datos de entrada para la predicción.
        models (tuple): Tupla con los modelos cargados (logistic, rf, xgb).
        
    Returns:
        dict: Diccionario con las predicciones de cada modelo.
    """
    # Extraer los modelos
    logistic_model, rf_model, xgb_model = models
    
    # Ejecutar las predicciones de forma concurrente
    logistic_result, rf_result, xgb_result = await asyncio.gather(
        predict_logistic_regression_async(data, logistic_model),
        predict_random_forest_async(data, rf_model),
        predict_xgboost_async(data, xgb_model)
    )
    
    # Devolver las predicciones como un diccionario
    return {
        "logistic_regression": logistic_result,
        "random_forest": rf_result,
        "xgboost": xgb_result
    }