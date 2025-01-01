from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
import pandas as pd
from app.v1.functions.logs_functions import clear_all_logs_byEmail, clear_logs_byId, fetch_logs, get_logs_byEmail
from app.v1.functions.shared_functions import verify_role


router = APIRouter()

@router.get("/user")
async def get_profile(email: str):
    # Verify role using email
    profile = await get_logs_byEmail(email)
    if not profile:
        raise HTTPException(status_code=404, detail="User not found")
    return profile

@router.get("/user_log")
async def get_profile(email: str):
    # Verify role using email
    profile = await get_logs_byEmail(email)
    if not profile:
        raise HTTPException(status_code=404, detail="User not found")
    return profile

@router.get("/clearall")
async def clear_all_logs(email: str):
    return await clear_all_logs_byEmail(email)

@router.get("/clearlog")
async def cleat_log_byId(email: str, id: int):
    return await clear_logs_byId(email, id)

# logs_api.py
@router.get("/user-activity")
async def get_user_activity_logs(email: str = None):
    # Fetch activity logs
    if email:
        logs = await get_logs_byEmail(email)
    else:
        logs = await fetch_logs()
    
    return logs
