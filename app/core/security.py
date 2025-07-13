from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
import os
from dotenv import load_dotenv

# Carga variables de entorno
load_dotenv()

# Configuración de seguridad
SECRET_KEY = os.getenv("SECRET_KEY", "secret-key-para-desarrollo")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Configuración para hashing de contraseñas
pwd_context = CryptContext(
    schemes=["argon2"],
    argon2__rounds=3,           # Debe coincidir con los logs (t=3)
    argon2__memory_cost=65536,  # Debe coincidir con los logs (m=65536)
    argon2__parallelism=4,      # Debe coincidir con los logs (p=4)
    deprecated="auto"
)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si una contraseña coincide con su versión hasheada"""
    try:
        print(f"🔍 [SECURITY DEBUG] Verificando contraseña:")
        print(f"  - Contraseña plana: '{plain_password}'")
        print(f"  - Tipo contraseña: {type(plain_password)}")
        print(f"  - Longitud contraseña: {len(plain_password)}")
        print(f"  - Hash almacenado: {hashed_password}")
        print(f"  - Tipo hash: {type(hashed_password)}")
        print(f"  - Longitud hash: {len(hashed_password)}")
        
        # Verificar que el hash tenga el formato correcto
        if not hashed_password.startswith('$argon2'):
            print(f"❌ [SECURITY ERROR] Hash no tiene formato Argon2: {hashed_password[:50]}...")
            return False
        
        # Realizar la verificación
        result = pwd_context.verify(plain_password, hashed_password)
        print(f"  - Resultado verificación: {result}")
        
        # Si falla, intentar generar un hash nuevo para comparar estructura
        if not result:
            new_hash = pwd_context.hash(plain_password)
            print(f"  - Hash nuevo generado: {new_hash}")
            print(f"  - Comparación estructural:")
            print(f"    * Hash almacenado: {hashed_password}")
            print(f"    * Hash nuevo:      {new_hash}")
        
        return result
        
    except Exception as e:
        print(f"❌ [SECURITY ERROR] Excepción en verify_password: {e}")
        print(f"  - Tipo excepción: {type(e)}")
        return False

def get_password_hash(password: str) -> str:
    """Genera un hash seguro de la contraseña"""
    try:
        print(f"🔍 [SECURITY DEBUG] Generando hash para: '{password}'")
        hash_result = pwd_context.hash(password)
        print(f"  - Hash generado: {hash_result}")
        return hash_result
    except Exception as e:
        print(f"❌ [SECURITY ERROR] Error generando hash: {e}")
        raise

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Crea un token JWT de acceso"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    """Decodifica y verifica un token JWT"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

# Función de utilidad para testing manual
def test_password_verification(password: str, stored_hash: str) -> bool:
    """Función de testing para verificar problemas con contraseñas"""
    print(f"\n🧪 [TEST] Prueba manual de verificación:")
    print(f"  - Contraseña: '{password}'")
    print(f"  - Hash almacenado: {stored_hash}")
    
    # Generar nuevo hash
    new_hash = get_password_hash(password)
    print(f"  - Hash nuevo: {new_hash}")
    
    # Verificar con hash almacenado
    verify_stored = verify_password(password, stored_hash)
    print(f"  - Verificación con hash almacenado: {verify_stored}")
    
    # Verificar con hash nuevo
    verify_new = verify_password(password, new_hash)
    print(f"  - Verificación con hash nuevo: {verify_new}")
    
    return verify_stored