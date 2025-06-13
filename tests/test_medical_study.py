import requests
import json
import random
import string
import time

# --- Configuración ---
BASE_URL = "http://localhost:8000"
USERS_ENDPOINT = f"{BASE_URL}/users/"
STUDIES_ENDPOINT = f"{BASE_URL}/medical_studies/"

# --- Funciones de Ayuda para una Salida Clara ---
def print_success(message):
    print(f"\033[92m✅ {message}\033[0m")

def print_error(message):
    print(f"\033[91m❌ {message}\033[0m")

def print_info(message):
    print(f"\033[94mℹ️ {message}\033[0m")

def generate_random_string(length=8):
    """Genera una cadena aleatoria para DNI y emails únicos."""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

# --- Fase 1: Preparación (Crear usuarios necesarios) ---
def setup_test_users():
    """
    Crea un doctor y un paciente para poder usarlos en la creación del estudio.
    Asumimos que role_id=2 es DOCTOR y role_id=3 es PATIENT.
    Ajusta estos IDs si son diferentes en tu sistema.
    """
    print_info("Preparando entorno: Creando usuarios de prueba (Doctor y Paciente)...")
    doctor_id = None
    patient_id = None
    
    try:
        # Crear Doctor
        rand_str_doc = generate_random_string()
        doctor_payload = {
            "name": "Doctor",
            "last_name": "DePrueba",
            "email": f"doctor.{rand_str_doc}@test.com",
            "dni": rand_str_doc.upper(),
            "password": "password123",
            "role_id": 2  # Asumiendo 2 = DOCTOR
        }
        response_doc = requests.post(USERS_ENDPOINT, json=doctor_payload)
        if response_doc.status_code == 201:
            doctor_id = response_doc.json()['id']
            print_success(f"Usuario Doctor creado con ID: {doctor_id}")
        else:
            print_error(f"No se pudo crear el Doctor. Status: {response_doc.status_code}, Body: {response_doc.text}")

        # Crear Paciente
        rand_str_pat = generate_random_string()
        patient_payload = {
            "name": "Paciente",
            "last_name": "DePrueba",
            "email": f"paciente.{rand_str_pat}@test.com",
            "dni": rand_str_pat.upper(),
            "password": "password123",
            "role_id": 3  # Asumiendo 3 = PATIENT
        }
        response_pat = requests.post(USERS_ENDPOINT, json=patient_payload)
        if response_pat.status_code == 201:
            patient_id = response_pat.json()['id']
            print_success(f"Usuario Paciente creado con ID: {patient_id}")
        else:
            print_error(f"No se pudo crear el Paciente. Status: {response_pat.status_code}, Body: {response_pat.text}")
    
    except requests.exceptions.RequestException as e:
        print_error(f"Error de conexión al crear usuarios: {e}")

    return doctor_id, patient_id

# --- Fase 2: Ejecución del Test Principal ---
def test_create_medical_study(doctor_id, patient_id):
    """
    Test para crear un estudio médico exitosamente.
    """
    print_info("\n🧪 Ejecutando test: Creación de estudio médico...")
    
    # Generar un código de acceso único para cada ejecución del test
    access_code = f"STUDY-{generate_random_string(6).upper()}"
    
    study_payload = {
        "access_code": access_code,
        "doctor_id": doctor_id,
        "patient_id": patient_id,
        "technician_id": None, # Opcional
        "clinical_data": "Paciente presenta síntomas de prueba para el test automatizado."
    }
    
    print_info(f"📤 Enviando datos para crear estudio:\n{json.dumps(study_payload, indent=2)}")

    try:
        response = requests.post(STUDIES_ENDPOINT, json=study_payload)
        
        print_info(f"Status Code: {response.status_code}")
        print_info(f"Response Body:\n{response.text}")

        if response.status_code == 201:
            print_success("¡Estudio médico creado exitosamente!")
            return response.json().get('id')
        else:
            print_error("Falló la creación del estudio médico.")
            return None

    except requests.exceptions.RequestException as e:
        print_error(f"Error de conexión al crear el estudio: {e}")
        return None

# --- Fase 3: Limpieza ---
def cleanup_data(study_id=None, doctor_id=None, patient_id=None):
    """
    Elimina los datos creados durante el test para mantener la BD limpia.
    """
    print_info("\n🧹 Limpiando datos de prueba...")
    if study_id:
        try:
            res = requests.delete(f"{STUDIES_ENDPOINT}{study_id}")
            if res.status_code == 200:
                print_success(f"Estudio {study_id} eliminado.")
            else:
                # Este endpoint puede que aún no devuelva 200, ajusta según tu implementación
                print_error(f"No se pudo eliminar el estudio {study_id}. Status: {res.status_code}")
        except requests.exceptions.RequestException as e:
            print_error(f"Error al eliminar estudio: {e}")

    if doctor_id:
        try:
            res = requests.delete(f"{USERS_ENDPOINT}{doctor_id}")
            if res.status_code == 200:
                print_success(f"Usuario Doctor {doctor_id} eliminado.")
            else:
                print_error(f"No se pudo eliminar al Doctor {doctor_id}. Status: {res.status_code}")
        except requests.exceptions.RequestException as e:
            print_error(f"Error al eliminar doctor: {e}")
            
    if patient_id:
        try:
            res = requests.delete(f"{USERS_ENDPOINT}{patient_id}")
            if res.status_code == 200:
                print_success(f"Usuario Paciente {patient_id} eliminado.")
            else:
                print_error(f"No se pudo eliminar al Paciente {patient_id}. Status: {res.status_code}")
        except requests.exceptions.RequestException as e:
            print_error(f"Error al eliminar paciente: {e}")

# --- Orquestador Principal ---
if __name__ == "__main__":
    print("="*50)
    print("🚀 INICIANDO TEST PARA POST /medical_studies/")
    print("="*50)
    
    doctor_id, patient_id = None, None
    study_id = None
    
    try:
        # 1. Crear los pre-requisitos
        doctor_id, patient_id = setup_test_users()

        # 2. Si los usuarios se crearon, ejecutar el test principal
        if doctor_id and patient_id:
            study_id = test_create_medical_study(doctor_id, patient_id)
        else:
            print_error("No se pudo continuar con el test de estudios debido a un fallo en la creación de usuarios.")

    finally:
        # 3. Limpiar todo lo creado, incluso si el test falló
        print_info("\nLa ejecución del test ha finalizado.")
        # Pequeña pausa para asegurar que la BD procesó todo
        time.sleep(1) 
        cleanup_data(study_id, doctor_id, patient_id)