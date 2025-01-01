from fastapi import APIRouter, Depends, HTTPException
from app.v1.functions.auth_functions import get_user_by_email
from app.v1.functions.user_functions import get_user_by_id, update_password, update_user_credentials, change_password, update_user_credentials_address, update_user_credentials_email, update_user_credentials_phone, validate_current_password
from app.v1.functions.shared_functions import verify_role, get_current_user
from app.v1.schema.user_schema import UserCredentialsAddress, UserCredentialsEmail, UserCredentialsPhone, UserProfile, UserCredentials, UpdatePassword

router = APIRouter()

@router.get("/profile")
async def get_profile(email: str):
    # Verify role using email
    
    profile = await get_user_by_email(email)
    if not profile:
        raise HTTPException(status_code=404, detail="User not found")
    return profile

@router.put("/profile/email")
async def update_profile(data: UserCredentialsEmail):
    # Verify role using email
    #await verify_role(data.email, "User")
    await update_user_credentials_email(data.email, data.new_email, data.ip_address)
    return {"message": "Profile updated successfully"}

@router.put("/profile/address")
async def update_profile(data: UserCredentialsAddress):
    # Verify role using email
    #await verify_role(data.email, "User")
    await update_user_credentials_address(data.email, data.new_address, data.ip_address)
    return {"message": "Profile updated successfully"}

@router.put("/profile/phoneNumber")
async def update_profile(data: UserCredentialsPhone):
    # Verify role using email
    #await verify_role(data.email, "User")
    await update_user_credentials_phone(data.email, data.new_phoneNumber, data.ip_address)
    return {"message": "Profile updated successfully"}

@router.put("/change-password")
async def change_password(email: str, data: UpdatePassword):
    # Verify role using email
    

    # Check if the current password is valid
    is_valid = await validate_current_password(email, data.current_password)
    if not is_valid:
        raise HTTPException(status_code=400, detail="Current password is incorrect")

    # Update the password
    await update_password(email, data.new_password)
    return {"message": "Password updated successfully"}
