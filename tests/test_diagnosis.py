import requests
import json
import random
import string
import time
import os

# --- 1. CONFIGURACIÓN PRINCIPAL ---
# ❗️❗️❗️ IMPORTANTE: Modifica esta línea para que apunte a tu archivo CSV de prueba.
# Puede ser una ruta absoluta o relativa a la ubicación de este script.
CSV_FILE_PATH = "/mnt/GitHub/miel-ia/notebooks/preprocessing/archivo_procesado_1.csv" 
# Por ejemplo: "data/sample_positive.csv" o "/home/user/proyecto/data/test.csv"


# --- Configuración de la API ---
BASE_URL = "http://localhost:8000"
USERS_ENDPOINT = f"{BASE_URL}/users/"
STUDIES_ENDPOINT = f"{BASE_URL}/medical_studies/"
DIAGNOSE_ENDPOINT = f"{BASE_URL}/diagnose/"


# --- Funciones de Ayuda para una Salida Clara ---
def print_header(title):
    print("\n" + "="*60)
    print(f"▶️  {title}")
    print("="*60)

def print_success(message):
    print(f"\033[92m✅ {message}\033[0m")

def print_error(message):
    print(f"\033[91m❌ {message}\033[0m")

def print_info(message):
    print(f"\033[94mℹ️  {message}\033[0m")

def generate_random_string(length=8):
    """Genera una cadena aleatoria para DNI y emails únicos."""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


# --- FASE DE PREPARACIÓN (SETUP) ---
def setup_test_environment():
    """
    Crea todos los recursos necesarios para ejecutar el test de diagnóstico.
    1. Un Doctor
    2. Un Paciente
    3. Un Estudio Médico asociado a ellos.
    Devuelve un diccionario con los IDs de los recursos creados.
    """
    print_header("FASE 1: PREPARANDO ENTORNO DE PRUEBA")
    created_ids = {"doctor_id": None, "patient_id": None, "study_id": None, "technician_id": None}

    try:
        # --- Crear Doctor (será el técnico que diagnostica también) ---
        rand_doc = generate_random_string()
        doctor_payload = {
            "name": "Doctor", "last_name": "Diagnóstico",
            "email": f"doc.diag.{rand_doc}@test.com", "dni": rand_doc.upper(),
            "password": "password123", "role_id": 2 # Asumiendo 2 = DOCTOR
        }
        response = requests.post(USERS_ENDPOINT, json=doctor_payload)
        if response.status_code == 201:
            created_ids["doctor_id"] = response.json()['id']
            created_ids["technician_id"] = created_ids["doctor_id"] # Usaremos el mismo doctor como técnico
            print_success(f"Usuario Doctor/Técnico creado con ID: {created_ids['doctor_id']}")
        else:
            raise Exception(f"No se pudo crear el Doctor. Status: {response.status_code}, Body: {response.text}")

        # --- Crear Paciente ---
        rand_pat = generate_random_string()
        patient_payload = {
            "name": "Paciente", "last_name": "Estudio",
            "email": f"pac.estudio.{rand_pat}@test.com", "dni": rand_pat.upper(),
            "password": "password123", "role_id": 3 # Asumiendo 3 = PATIENT
        }
        response = requests.post(USERS_ENDPOINT, json=patient_payload)
        if response.status_code == 201:
            created_ids["patient_id"] = response.json()['id']
            print_success(f"Usuario Paciente creado con ID: {created_ids['patient_id']}")
        else:
            raise Exception(f"No se pudo crear el Paciente. Status: {response.status_code}, Body: {response.text}")
            
        # --- Crear Estudio Médico ---
        access_code = f"DIAGTEST-{generate_random_string(6).upper()}"
        study_payload = {
            "access_code": access_code,
            "doctor_id": created_ids["doctor_id"],
            "patient_id": created_ids["patient_id"],
            "clinical_data": "Estudio de prueba para el flujo de diagnóstico."
        }
        response = requests.post(STUDIES_ENDPOINT, json=study_payload)
        if response.status_code == 201:
            created_ids["study_id"] = response.json()['id']
            print_success(f"Estudio Médico creado con ID: {created_ids['study_id']} y estado PENDING.")
        else:
            raise Exception(f"No se pudo crear el Estudio. Status: {response.status_code}, Body: {response.text}")

        return created_ids

    except Exception as e:
        print_error(f"Falló la preparación del entorno: {e}")
        return None
    
    # --- FASE 2.5: TEST DE ACTUALIZACIÓN CON PATCH ---
def test_update_study_with_patch(created_ids):
    """
    Test para actualizar un estudio médico existente usando PATCH.
    Simula la actualización del estado y la adición de los resultados del ML.
    """
    print_header("FASE 2: ACTUALIZANDO ESTUDIO MÉDICO CON PATCH")
    
    study_id = created_ids.get("study_id")
    if not study_id:
        print_error("No se puede ejecutar el test PATCH sin un study_id válido.")
        return False

    # 1. Simular un resultado que vendría del pipeline de ML
    #    Este es un diccionario de ejemplo.
    ml_results_payload = {
        "final_diagnosis": "Positivo para Mieloma Múltiple",
        "classification_level": 2,
        "details": {
            "binary_model_votes": {"rf": 1, "xgb": 1, "log": 1},
            "classification_details": {
                "was_classified": True,
                "model_votes": {"rf": 2, "xgb": 2, "log": 1},
                "final_level_assigned": 2
            }
        }
    }
    
    # 2. El payload para PATCH solo contiene los campos que queremos cambiar.
    patch_payload = {
        "status": "HECHO", # o "COMPLETED", según lo tengas en tu servicio.
        "ml_results": json.dumps(ml_results_payload) # El servicio espera un string JSON.
    }
    
    print_info(f"📤 Enviando petición a PATCH {STUDIES_ENDPOINT}{study_id}")
    print_info(f"   - Body: {json.dumps(patch_payload, indent=2, ensure_ascii=False)}")

    try:
        # 3. Usar requests.patch para enviar la petición
        response = requests.patch(f"{STUDIES_ENDPOINT}{study_id}", json=patch_payload)
        
        print_info(f"Status Code: {response.status_code}")
        
        response_json = response.json()
        print_info("Response Body:")
        print(json.dumps(response_json, indent=2, ensure_ascii=False))

        # 4. Verificar que la actualización fue exitosa
        if response.status_code == 200 and response_json.get("status") == "HECHO":
            print_success("¡Verificación exitosa! El estudio fue actualizado correctamente con PATCH.")
            return True
        else:
            print_error("Falló la actualización del estudio con PATCH.")
            return False

    except requests.exceptions.RequestException as e:
        print_error(f"Error de conexión durante la actualización con PATCH: {e}")
        return False



# --- FASE DE EJECUCIÓN DEL TEST ---
def run_diagnosis_test(created_ids):
    """
    Ejecuta el test principal contra el endpoint /diagnose.
    """
    print_header("FASE 2: EJECUTANDO TEST DE DIAGNÓSTICO")

    if not os.path.exists(CSV_FILE_PATH):
        print_error(f"El archivo CSV de prueba no se encuentra en la ruta: '{CSV_FILE_PATH}'")
        return

    study_id = created_ids["study_id"]
    technician_id = created_ids["technician_id"]
    
    # Preparamos la petición multipart/form-data
    # 'files' para el archivo, 'data' para otros campos del formulario
    with open(CSV_FILE_PATH, 'rb') as f:
        files = {'file': (os.path.basename(CSV_FILE_PATH), f, 'text/csv')}
        data = {'user_id': technician_id}
        
        print_info(f"📤 Enviando petición a POST {DIAGNOSE_ENDPOINT}{study_id}")
        print_info(f"   - user_id (form-data): {technician_id}")
        print_info(f"   - file (form-data): {os.path.basename(CSV_FILE_PATH)}")
        
        try:
            response = requests.post(f"{DIAGNOSE_ENDPOINT}{study_id}", files=files, data=data)
            
            print_info(f"Status Code: {response.status_code}")
            
            # Intentamos formatear la respuesta como JSON para una lectura más fácil
            try:
                response_json = response.json()
                print_info("Response Body:")
                print(json.dumps(response_json, indent=2, ensure_ascii=False))

                # Verificaciones clave
                if response.status_code == 200:
                    if response_json.get("status") == "COMPLETED":
                        print_success("¡Verificación exitosa! El estado del estudio es 'COMPLETED'.")
                    else:
                        print_error("Fallo en la verificación: El estado del estudio NO es 'COMPLETED'.")
                    
                    if response_json.get("ml_results"):
                        print_success("¡Verificación exitosa! El campo 'ml_results' contiene datos.")
                    else:
                        print_error("Fallo en la verificación: El campo 'ml_results' está vacío.")
                else:
                    print_error("La petición de diagnóstico falló.")

            except json.JSONDecodeError:
                print_error("La respuesta no es un JSON válido.")
                print(response.text)

        except requests.exceptions.RequestException as e:
            print_error(f"Error de conexión durante el diagnóstico: {e}")

# --- FASE DE LIMPIEZA ---
def cleanup_test_environment(created_ids):
    """
    Elimina todos los recursos creados durante el test.
    """
    if not created_ids:
        return
        
    print_header("FASE 3: LIMPIANDO ENTORNO DE PRUEBA")
    
    # Eliminar en orden inverso para respetar las Foreign Keys
    if created_ids.get("study_id"):
        try:
            res = requests.delete(f"{STUDIES_ENDPOINT}{created_ids['study_id']}")
            if res.status_code == 200:
                print_success(f"Estudio {created_ids['study_id']} eliminado.")
            else:
                print_error(f"No se pudo eliminar el estudio {created_ids['study_id']}. Status: {res.status_code}, Body: {res.text}")
        except requests.exceptions.RequestException as e:
            print_error(f"Error al eliminar estudio: {e}")

    if created_ids.get("doctor_id"):
        try:
            res = requests.delete(f"{USERS_ENDPOINT}{created_ids['doctor_id']}")
            if res.status_code == 200:
                print_success(f"Usuario Doctor {created_ids['doctor_id']} eliminado.")
            else:
                print_error(f"No se pudo eliminar al Doctor {created_ids['doctor_id']}. Status: {res.status_code}, Body: {res.text}")
        except requests.exceptions.RequestException as e:
            print_error(f"Error al eliminar doctor: {e}")
            
    if created_ids.get("patient_id") and created_ids["patient_id"] != created_ids["doctor_id"]:
        try:
            res = requests.delete(f"{USERS_ENDPOINT}{created_ids['patient_id']}")
            if res.status_code == 200:
                print_success(f"Usuario Paciente {created_ids['patient_id']} eliminado.")
            else:
                print_error(f"No se pudo eliminar al Paciente {created_ids['patient_id']}. Status: {res.status_code}, Body: {res.text}")
        except requests.exceptions.RequestException as e:
            print_error(f"Error al eliminar paciente: {e}")


# --- ORQUESTADOR PRINCIPAL ---
if __name__ == "__main__":
    created_resources = None
    test_passed = False
    
    try:
        # FASE 1: Crea todos los recursos necesarios
        created_resources = setup_test_environment()
        
        # FASE 2: Si la preparación fue exitosa, ejecuta el test de actualización
        if created_resources:
            # Pausa para asegurar que la transacción de creación se complete
            time.sleep(1) 
            test_passed = test_update_study_with_patch(created_resources)
            
    except Exception as e:
        print_error(f"Ocurrió un error inesperado durante la ejecución del test: {e}")
    finally:
        # FASE 3: La limpieza se ejecuta siempre, incluso si el test falló
        if created_resources:
            cleanup_test_environment(created_resources)
        
        print("\nTest finalizado.")
        if test_passed:
            print_success("RESULTADO FINAL: El flujo de actualización funciona correctamente.")
        else:
            print_error("RESULTADO FINAL: Hubo fallos en el flujo de actualización.")

