from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
import pandas as pd
from app.database import database_control
from app.v1.functions.logs_functions import fetch_logs
from app.v1.functions.shared_functions import get_current_user, verify_role
from app.v1.schema.user_schema import AdminUpdateRole, AdminUpdateUser

router = APIRouter()

@router.get("/users")
async def get_all_users():
    # Ensure the user is an admin
    # await verify_role(user_id, "Admin")
    query = "SELECT id, username, email, phone_number as phone, role FROM sdm.users"
    return await database_control.fetch_all(query)

@router.put("/users/{target_user_id}")
async def update_user(target_user_id: int, data: AdminUpdateUser, user_id: int = Depends(get_current_user)):
    # Ensure the requester is an admin
    await verify_role(user_id, "ADMIN")
    query = """
    UPDATE sdm.users
    SET email = :email, role = :role
    WHERE id = :id
    """
    await database_control.execute(query, {"id": target_user_id, "email": data.email, "role": data.role})
    return {"message": "User updated successfully"}

@router.put("/user-role-status")
async def update_user(data: AdminUpdateRole):
    # Ensure the requester is an admin
    # await verify_role(int(data.user_id), "Admin")
    query = """
    UPDATE sdm.users
    SET role = :role
    WHERE id = :id
    """
    await database_control.execute(query, {"id": data.user_id, "role": data.new_role})
    return {"message": "User updated successfully"}

@router.get("/logs/export")
async def export_logs():
    logs = await fetch_logs()
    headers = list(logs[0].keys())
    rows = [log.values() for log in logs]
    df = pd.DataFrame(rows, columns=headers)
    file_path = "exported_logs.xlsx"
    with pd.ExcelWriter(file_path, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Logs")

        # Access the workbook and worksheet
        workbook = writer.book
        worksheet = writer.sheets["Logs"]

        # Adjust column widths based on header lengths
        for i, column in enumerate(df.columns):
            column_width = max(df[column].astype(str).map(len).max(), len(column)) + 2
            worksheet.set_column(i, i, column_width)
    headers = {"Content-Disposition": f'attachment; filename="{file_path}"'}
    return FileResponse(file_path, headers=headers)

