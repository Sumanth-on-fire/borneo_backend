from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import connect_to_database, disconnect_to_database
from app.v1.api.routes import  admin_api, auth_api, logs_api, user_api

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_database()
    try:
        yield
    finally:
        await disconnect_to_database()

app = FastAPI(
    title="Secure API",
    version="0.0.0.1",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*", 'http://localhost:3000/'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_api.router, prefix="/v1/api/auth", tags=["Authentication_API"])
app.include_router(user_api.router, prefix="/v1/api/user", tags=["User_API"])
app.include_router(admin_api.router, prefix="/v1/api/admin", tags=["Admin_API"])
app.include_router(logs_api.router, prefix="/v1/api/log", tags=["Logs_API"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Secure Platform API"}
