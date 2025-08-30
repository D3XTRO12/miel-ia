from click import DateTime
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

# Configuración para hashing de contraseñas - CORREGIDA
pwd_context = CryptContext(
    schemes=["argon2"],
    argon2__time_cost=3,        # CORREGIDO: era argon2__rounds
    argon2__memory_cost=65536,  # Debe coincidir con los logs (m=65536)
    argon2__parallelism=4,      # Debe coincidir con los logs (p=4)
    deprecated="auto"
)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si una contraseña coincide con su versión hasheada"""
    try:
        print(f"🔍 [SECURITY DEBUG] Verificando contraseña:")
        print(f"  - Contraseña plana: '{plain_password}'")
        print(f"  - Hash almacenado: {hashed_password[:50]}...")
        
        # Verificar que el hash tenga el formato correcto
        if not hashed_password.startswith('$argon2'):
            print(f"❌ [SECURITY ERROR] Hash no tiene formato Argon2")
            return False
        
        # Realizar la verificación
        result = pwd_context.verify(plain_password, hashed_password)
        print(f"  - Resultado verificación: {result}")
        
        # Si falla, mostrar info adicional para debug
        if not result:
            print(f"  - ⚠️ Verificación fallida, intentando diagnóstico...")
            try:
                # Generar hash nuevo para comparar parámetros
                new_hash = pwd_context.hash(plain_password)
                print(f"  - Hash generado ahora: {new_hash[:50]}...")
                
                # Extraer parámetros del hash almacenado
                stored_params = hashed_password.split('$')[3] if len(hashed_password.split('$')) > 3 else "unknown"
                new_params = new_hash.split('$')[3] if len(new_hash.split('$')) > 3 else "unknown"
                
                print(f"  - Parámetros almacenados: {stored_params}")
                print(f"  - Parámetros actuales: {new_params}")
                
                # SOLUCIÓN DE EMERGENCIA: Si los parámetros son diferentes, rehash
                if stored_params != new_params:
                    print("  - 🔄 Parámetros diferentes detectados, necesita rehash")
                    # En este caso, podríamos asumir que la contraseña es correcta
                    # y actualizar el hash (solo para desarrollo/migración)
                    
            except Exception as debug_e:
                print(f"  - Error en diagnóstico: {debug_e}")
        
        return result
        
    except Exception as e:
        print(f"❌ [SECURITY ERROR] Excepción en verify_password: {e}")
        return False

def get_password_hash(password: str) -> str:
    """Genera un hash seguro de la contraseña"""
    try:
        print(f"🔍 [SECURITY DEBUG] Generando hash para contraseña de {len(password)} caracteres")
        hash_result = pwd_context.hash(password)
        print(f"  - Hash generado: {hash_result[:50]}...")
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

# FUNCIÓN DE EMERGENCIA PARA RESETEAR CONTRASEÑA
def emergency_password_reset(email: str, new_password: str):
    """
    Función de emergencia para resetear contraseña en desarrollo
    """
    try:
        from app.core.db import engine
        from sqlalchemy import text
        
        new_hash = get_password_hash(new_password)
        
        with engine.connect() as conn:
            result = conn.execute(
                text("UPDATE users SET password = :new_hash WHERE email = :email"),
                {"new_hash": new_hash, "email": email}
            )
            conn.commit()
            
        print(f"✅ Contraseña reseteada para {email}")
        return True
        
    except Exception as e:
        print(f"❌ Error reseteando contraseña: {e}")
        return False