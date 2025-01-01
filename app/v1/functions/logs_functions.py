# v1/functions/logs.py

from datetime import datetime
from fastapi import HTTPException, Request
from app.database import database_control
import pandas as pd

async def add_activity_log(action: str, email: str, request: str):
    query = """
        INSERT INTO sdm.activity_logs (email, ip_address, action, timestamp)
        VALUES (:email, :ip_address, :action, :timestamp)
    """
    values = {
        "email": email,
        "ip_address": request,
        "action": action,
        "timestamp": datetime.utcnow()
    }
    await database_control.execute(query=query, values=values)

async def get_logs_byEmail(email: str):
    query ="""
        SELECT * from sdm.activity_logs where email=:email        
    """
    values = {
          "email": email
    }

    result = await database_control.fetch_all(query=query, values=values)
    return result

async def clear_all_logs_byEmail(email: str):
    query="""
        DELETE from sdm.activity_logs where email=:email
    """
    values = {
        "email": email
    }

    try:
        await database_control.execute(query=query, values=values)
    except:
        raise HTTPException(status_code=404, detail="Not able to delete all the logs") 
    return True

async def clear_logs_byId(email: str, id: int):
    query="""
     DELETE from sdm.activity_logs where id=:id and email=:email
"""
    values = {
        "email": email,
        "id": id
    }

    try:
        await database_control.execute(query=query, values=values)
    except:
        raise HTTPException(status_code=404, detail="Not able to delete log based on the id")
    
    return True

async def fetch_logs():
    query = "SELECT * FROM sdm.activity_logs"
    return await database_control.fetch_all(query)

async def export_logs_to_excel():
    logs = await fetch_logs()
    df = pd.DataFrame(logs)
    file_path = "exported_logs.xlsx"
    df.to_excel(file_path, index=False)
    return {"file_path": file_path}