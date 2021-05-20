from passlib.context import CryptContext
from models.jwt_user import JWTUser
from fastapi import Depends
from util.const import *
from datetime import datetime, timedelta
import jwt
from fastapi.security import OAuth2PasswordBearer
from starlette.status import HTTP_401_UNAUTHORIZED

my_ctx = CryptContext(schemes=['sha256_crypt'])
oauth_schema = OAuth2PasswordBearer(tokenUrl="/token")


def get_hashed_password(password):
    return my_ctx.hash(password);


def verify_password(password, hashed_password):
    try:
        return my_ctx.verify(password, hashed_password)
    except:
        return False


user_admin = JWTUser(**{
    "username": "frankadmin",
    "password": get_hashed_password("pass1"),
    "disabled": False,
    "role": "admin"
})


# Authenticate users given username and password
def authenticate_user(user: JWTUser):
    if user.username == user_admin.username:
        if verify_password(user.password, user_admin.password):
            user.role = "admin"
            return user

    return None


# Create JWT access token
def create_jwt_token(user: JWTUser):
    payload = {
        "sub": user.username,
        "role": user.role,
        "exp": datetime.utcnow() + timedelta(minutes=JWT_EXPIRATION_TIME_MINUTES)
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


# Check if user has administrative permissions
def is_admin(role):
    if role == "admin":
        return True

    return False


# Check whether JWT token is correct
def validate_token(token: str = Depends(oauth_schema)):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        username = payload.get("sub")
        role = payload.get("role")
        expiration = payload.get("exp")
        if username == user_admin.username and datetime.utcnow() < datetime.utcfromtimestamp(expiration):
            return is_admin(role)
    except:
        return False

    return False
