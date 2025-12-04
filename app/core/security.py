from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt
from app.core.config import JWT_SECRET_KEY, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    password = password[:72]
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    plain = plain[:72]
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data.update({"exp": expire})
    return jwt.encode(data, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)