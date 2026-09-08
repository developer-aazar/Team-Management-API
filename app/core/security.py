import bcrypt
from jose import jwt
import bcrypt 
from datetime import datetime , timedelta
from app.core.config import settings

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8') , salt)
    return hashed_password.decode('utf-8')

def verify_password(plain_password: str , hashed_password: str):
    return bcrypt.checkpw(plain_password.encode('utf-8') , hashed_password.encode('utf-8'))

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode , settings.secret_key , algorithm=settings.algorithm)
    return encoded_jwt
    
def verify_access_token(token: str) -> dict | None:
        payload = jwt.decode(token , settings.secret_key , algorithms=[settings.algorithm])
        return payload
