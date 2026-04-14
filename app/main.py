from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.config import get_settings
from app.core.database import Database

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


app.include_router(api_router, prefix=settings.api_v1_prefix)

