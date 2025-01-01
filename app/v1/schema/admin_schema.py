from pydantic import BaseModel
from enum import Enum

class UserRole(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"

class RoleChangeRequest(BaseModel):
    user_id: int
    new_role: UserRole
