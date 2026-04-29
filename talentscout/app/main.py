from fastapi import FastAPI
from app.api.routes import roles, pipeline, reports
from app.api.deps import fastapi_users, auth_backend, create_db_and_tables
from app.models.schemas import UserRead, UserCreate
from app.models.db import User
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(title="TalentScout AI", lifespan=lifespan)

# Auth Routes
app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate), prefix="/auth", tags=["auth"]
)

# App Routes
app.include_router(roles.router)
app.include_router(pipeline.router)
app.include_router(reports.router)

@app.get("/")
def root():
    return {"message": "Welcome to TalentScout AI"}
