from jose import JWTError, jwt
from datetime import datetime, timedelta

SECRET_KEY = "1c5e4bb288aadf456ff72d53cef19982fbc1b4e67ad1d903d15dcc603ae160f0"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    # Copy the data to encode so that we don't modify the original
    to_encode = data.copy()
    # Here you would add expiration time to the token if needed
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

