from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.regularizers import l2

def create_model(input_dim=80):
    """
    Crea un modelo de regresión logística multiclase (3 clases) usando Keras.
    
    Args:
        input_dim: Dimensión de la capa de entrada (número de características)
        
    Returns:
        Modelo de Keras compilado para clasificación multiclase (clases 1, 2, 3)
    """
    model = Sequential()
    # Capa de entrada
    model.add(Input(shape=(input_dim,)))
    
    # Capas ocultas
    model.add(Dense(64, activation='relu', kernel_regularizer=l2(0.005)))  # Aumentar L2
    model.add(Dropout(0.5))  # Más agresivo
    model.add(Dense(32, activation='relu', kernel_regularizer=l2(0.005)))
    model.add(Dropout(0.3))

        
    # Capa de salida para 3 clases
    # Usamos 3 neuronas (una por clase) con activación softmax
    model.add(Dense(3, activation='softmax'))
    
    # Configuramos el optimizador con una tasa de aprendizaje ligeramente reducida
    optimizer = Adam(learning_rate=0.0005)
    
    
    # Compilamos el modelo
    # Para multiclase usamos categorical_crossentropy (en lugar de binary_crossentropy)
    model.compile(
        optimizer=optimizer,
        loss='sparse_categorical_crossentropy',  # Para etiquetas de clase enteras (1, 2, 3)
        metrics=['accuracy']
    )
    
    return model