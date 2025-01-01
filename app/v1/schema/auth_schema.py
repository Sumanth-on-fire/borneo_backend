from pydantic import BaseModel, EmailStr

class LoginRequest(BaseModel):
    username: str
    password: str

class SignupRequest(BaseModel):
    username: str
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    email: str
    role: str

class LoginSchema(BaseModel):
    username: str
    password: str

class SignupSchema(BaseModel):
    username: str
    email: EmailStr
    password: str