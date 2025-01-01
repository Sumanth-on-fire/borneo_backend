import jwt
from datetime import datetime, timedelta
from hashlib import sha256
from app.database import database_control
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "default_key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

async def authenticate_user(username: str, password: str):
    hashed_password = sha256(password.encode()).hexdigest()
    query = "SELECT id, email, role FROM sdm.users WHERE username = :username AND password = :password"
    user = await database_control.fetch_one(query, {"username": username, "password": hashed_password})
    return user

async def create_user(data):
    query = """
    INSERT INTO sdm.users (username, email, password, role)
    VALUES (:username, :email, :password, :role)
    """
    hashed_password = sha256(data.password.encode()).hexdigest()
    await database_control.execute(query, {
        "username": data.username,
        "email": data.email,
        "password": hashed_password,
        "role": "User",  # Default role
    })

async def get_user_by_email(email: str):
    query = "SELECT id, username, email, role, phone_number, address, status FROM sdm.users WHERE email = :email"
    return await database_control.fetch_one(query, {"email": email})

# def create_access_token(user_id: int) -> str:
#     """
#     Generates a JWT access token for a given user ID.
#     """
#     expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     payload = {"sub": user_id, "exp": expire}
#     token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
#     return token

# async def authenticate_user(username, password):
#     hashed_password = sha256(password.encode()).hexdigest()
#     query = "SELECT * FROM sdm.users WHERE username = :username AND password = :password"
#     return await database_control.fetch_one(query, {"username": username, "password": hashed_password})

def create_access_token(user_id, role):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": user_id, "role": role, "exp": expire}
    return jwt.encode(payload, key=SECRET_KEY, algorithm=ALGORITHM)

