# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Dense
# from tensorflow.keras.optimizers import Adam

# def create_model(input_dim=80):
#     model = Sequential()
#     model.add(Dense(32, activation='relu', input_dim=input_dim))
#     model.add(Dense(1, activation='sigmoid'))
#     model.compile(optimizer=Adam(), loss='binary_crossentropy', metrics=['accuracy'])
#     return model


from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.optimizers import Adam

def create_model(input_dim=80):
    """
    Crea un modelo de regresión logística usando Keras.
    
    Args:
        input_dim: Dimensión de la capa de entrada (número de características)
        
    Returns:
        Modelo de Keras compilado
    """
    model = Sequential()
    # Reemplazar input_dim con una capa Input correcta
    model.add(Input(shape=(input_dim,)))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(optimizer=Adam(), loss='binary_crossentropy', metrics=['accuracy'])
    return model