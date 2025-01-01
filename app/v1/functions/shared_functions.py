import os
from dotenv import load_dotenv
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
import jwt
from app.database import database_control

# Load environment variables
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/auth/token")

async def verify_role(email: str, required_role: str):
    query = "SELECT role FROM sdm.users WHERE email = :email"
    user = await database_control.fetch_one(query, {"email": email})
    if not user or user["role"] != required_role:
        raise HTTPException(status_code=403, detail="Unauthorized")
    return user

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")  # The 'sub' claim contains the user_id
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
