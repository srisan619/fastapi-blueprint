from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone

SECRET_KEY =""
ALGORITHM ="HS256"
ACCESS_TOKEN_EXPIRY=60 
pwd_context = CryptContext(schemes=["bcrypt"])

def hash_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    payload_data = data.copy()
    expire = (datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRY))
    payload_data.update({"exp": expire})
    encoded_jwt = jwt.encode(payload_data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
