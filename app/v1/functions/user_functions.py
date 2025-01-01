from fastapi import HTTPException
from app.database import database_control
from hashlib import sha256
from app.v1.functions.logs_functions import add_activity_log

async def get_user_by_id(user_id: int):
    query = "SELECT id, username, email, address, phone_number, role FROM sdm.users WHERE id = :id"
    return await database_control.fetch_one(query, {"id": user_id})

async def update_user_credentials(email: str, new_email: str, address: str, phone_number: str):
    query = """
    UPDATE sdm.users
    SET email = :new_email, address = :address, phone_number = :phone_number
    WHERE email = :email
    """
    await database_control.execute(query, {
        "email": email,
        "new_email": new_email,
        "address": address,
        "phone_number": phone_number,
    })

async def update_user_credentials_email(email: str, new_email: str, request: str):
    query = """
    UPDATE sdm.users
    SET email = :new_email
    WHERE email = :email
    """
    try:
        await database_control.execute(query, {
            "email": email,
            "new_email": new_email,
        })
    except: 
        raise HTTPException(status_code=404, detail="Unable to update the user email")

    await add_activity_log("changed email", email, request)
    return {"message": "Email updated successfully"}

async def update_user_credentials_address(email: str, address: str, request: str):
    query = """
    UPDATE sdm.users
    SET address = :address
    WHERE email = :email
    """
    try:
        await database_control.execute(query, {
            "address": address,
            "email": email
        })
    except:
        raise HTTPException(status_code=404, detail="Unable to update address successfully")
    
    await add_activity_log("address update", email, request)
    return {"message": "Address updated successfully"}

async def update_user_credentials_phone(email: str, phone_number: str, request: str):
    query = """
    UPDATE sdm.users
    SET phone_number = :phone_number
    WHERE email = :email
    """
    try:
        await database_control.execute(query, {
            "email": email,
            "phone_number": phone_number,
        })
    except:
        raise HTTPException(status_code=404, detail="Could not add user credentials !!")

    await add_activity_log("changed phone number", email, request)
    return {"message": "Phone number updated successfully"}

async def change_password(user_id: int, new_password: str):
    query = "UPDATE sdm.users SET password = :new_password WHERE id = :id"
    await database_control.execute(query, {"id": user_id, "new_password": new_password})

async def update_password(email: str, new_password: str):
    query = """
    UPDATE sdm.users
    SET password = :new_password
    WHERE email = :email
    """
    await database_control.execute(query, {
        "email": email,
        "new_password": new_password,
    })

async def validate_current_password(email: str, current_password: str) -> bool:
    hashed_password = sha256(current_password.encode()).hexdigest()
    query = "SELECT id FROM sdm.users WHERE email = :email AND password = :hashed_password"
    user = await database_control.fetch_one(query, {
        "email": email,
        "hashed_password": hashed_password
    })
    return user is not None
