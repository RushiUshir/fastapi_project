from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import get_settings
from app.core.database import Database
from app.routes.marriage_routes import router as marriage_router

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    database = Database.get_instance()
    await database.connect()
    yield
    await database.close()


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan,
)

app.include_router(marriage_router)
