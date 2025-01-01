import databases
from urllib.parse import quote_plus

username = "secure_data_management_user"
password = "WTiwxNqmYA3KIKXrJkXYCxCRIzICwOuL"
host = "dpg-cte2m1tds78s739hplr0-a.oregon-postgres.render.com"
port = "5432"
database_dev = "secure_data_management"
encoded_password = quote_plus(password)
database_url_control = f"postgresql://{username}:{encoded_password}@{host}:{port}/{database_dev}"

database_control = databases.Database(database_url_control)

async def connect_to_database():
    if not database_control.is_connected:
        await database_control.connect()

async def disconnect_to_database():
    if database_control.is_connected:
        await database_control.disconnect()
