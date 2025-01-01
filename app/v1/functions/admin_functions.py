from app.database import database_control

async def assign_role(user_id, new_role):
    query = "UPDATE sdm.users SET role = :new_role WHERE id = :user_id"
    await database_control.execute(query, {"new_role": new_role, "user_id": user_id})
    return True
