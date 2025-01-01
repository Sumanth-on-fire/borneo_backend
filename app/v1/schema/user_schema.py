from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserProfile(BaseModel):
    id: int
    username: str
    email: EmailStr
    address: Optional[str]
    phone_number: Optional[str]
    role: str

class UserCredentials(BaseModel):
    current_email: Optional[EmailStr]
    new_email: Optional[EmailStr]
    address: Optional[str]
    phone_number: Optional[str] = Field(None, max_length=15)

class UserCredentialsEmail(BaseModel):
    email: Optional[EmailStr]
    new_email: Optional[EmailStr]
    ip_address: str

class UserCredentialsAddress(BaseModel):
    email: Optional[EmailStr]
    new_address: Optional[str]
    ip_address: str

class UserCredentialsPhone(BaseModel):
    email: Optional[EmailStr]
    new_phoneNumber: Optional[str]
    ip_address: str

class UpdatePassword(BaseModel):
    current_password: str = Field(..., min_length=8, max_length=32)
    new_password: str = Field(..., min_length=8, max_length=32)

class AdminUpdateUser(BaseModel):
    email: Optional[EmailStr]
    role: Optional[str]

class AdminUpdateRole(BaseModel):
    user_id: int
    new_role: Optional[str]

