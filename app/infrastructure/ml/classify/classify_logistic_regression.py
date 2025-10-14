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
    model.add(Input(shape=(input_dim,)))
    
    model.add(Dense(64, activation='relu', kernel_regularizer=l2(0.005)))  
    model.add(Dropout(0.5))  
    model.add(Dense(32, activation='relu', kernel_regularizer=l2(0.005)))
    model.add(Dropout(0.3))

    model.add(Dense(3, activation='softmax'))
    
    optimizer = Adam(learning_rate=0.0005)

    model.compile(
        optimizer=optimizer,
        loss='sparse_categorical_crossentropy', 
        metrics=['accuracy']
    )
    
    return model