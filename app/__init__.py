import sys
import os

# Agregar el directorio app al path para imports absolutos
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)