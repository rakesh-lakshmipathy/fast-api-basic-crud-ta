from datetime import datetime, timedelta

from jose import jwt
from jose.exceptions import JWTError
from pwdlib import PasswordHash

from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"

# Demo username and password
USERNAME = "admin"
PASSWORD = "admin123"

password_hash = PasswordHash.recommended()
hashed_password = password_hash.hash(PASSWORD)

security = HTTPBearer()


# Verify username and password
def authenticate_user(username: str, password: str):

    if username == USERNAME and password_hash.verify(
        password, hashed_password
    ):
        return True

    return False


# Generate JWT token
def create_token(username: str):

    expire = datetime.utcnow() + timedelta(minutes=30)

    data = {
        "sub": username,
        "exp": expire
    }

    token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    return token


# Verify JWT token
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("sub")

        if username != USERNAME:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        return username

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )