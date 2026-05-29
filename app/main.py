from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.database import MongoDB
from app.routes.health_route import router as health_router
from app.routes.user_route import router as user_router
from contextlib import asynccontextmanager
from app.core.database import MongoDB
from pymongo import ASCENDING
from fastapi.middleware.cors import CORSMiddleware
import app.utils.cloudinary_config

@asynccontextmanager
async def lifespan(app: FastAPI):
    await MongoDB.connect_db()
    db = MongoDB.get_database()

    # Create users collection indexes
    await db.users.create_index(
        [("email", ASCENDING)],
        unique=True
    )

    await db.users.create_index(
        [("mobile", ASCENDING)],
        unique=True
    )

    await db.users.create_index(
        [("created_at", ASCENDING)]
    )

    yield
    await MongoDB.close_db()


app = FastAPI(
    title="Production FastAPI MongoDB",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(user_router)