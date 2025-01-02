from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from app.v1.functions.auth_functions import authenticate_user, autheticate_and_change_password, create_access_token, create_user, get_user_by_email
from app.database import database_control
from app.v1.functions.logs_functions import add_activity_log
from app.v1.schema.auth_schema import LoginSchema, LogoutSchema, SignupSchema, TokenResponse, UpdatePasswordSchema
import jwt
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants
SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")  # Replace for production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/api/auth/token")

router = APIRouter()

# Helper to create JWT tokens
def generate_token(user_id: int) -> str:
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": user_id, "exp": expire}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

@router.post("/login")
async def login(data: LoginSchema):
    user = await authenticate_user(data.username, data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token(user["id"], user["role"])
    
    # Record login activity
    await add_activity_log("Login", user["email"], data.ip_address)
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "email": user["email"],
        "role": user["role"],
    }

@router.post("/logout")
async def logout(data: LogoutSchema):
    # Record logout activity
    await add_activity_log("LOGOUT", data.username, data.ip_address)
    return {"message": "User logged out successfully"}

@router.post("/signup", response_model=TokenResponse)
async def signup(data: SignupSchema):
    # Check if email is already in use
    existing_user = await get_user_by_email(data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already in use")

    # Create a new user
    await create_user(data)

    await add_activity_log("Login", data.email, data.ip_address)

    # Fetch the newly created user's details
    new_user = await get_user_by_email(data.email)
    if not new_user:
        raise HTTPException(status_code=500, detail="Failed to create user")

    # Generate JWT token for the new user
    token = create_access_token(new_user["id"], new_user['role'])

    return {
        "access_token": token,
        "token_type": "bearer",
        "email": new_user["email"],  # Include email for frontend storage
        "role": new_user['role']
    }


@router.get("/profile")
async def get_profile(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")

        query = "SELECT id, username, email, role FROM sdm.users WHERE id = :id"
        user = await database_control.fetch_one(query, {"id": user_id})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")


@router.post("/updatepassword")
async def updatePassword(data: UpdatePasswordSchema):
    return await autheticate_and_change_password(data.email, data.current_password, data.new_password)
