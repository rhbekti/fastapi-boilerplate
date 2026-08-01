from fastapi import FastAPI
from src.core.logging import setup_logging
from src.core.exceptions import setup_exception_handlers
from src.core.middlewares import UnifiedResponseMiddleware
from contextlib import asynccontextmanager
from src.core.dependencies import init_db_engine, close_db_engine
from sqlmodel import SQLModel
from src.user.router import router as user_router

setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create Lifespan"""
    await init_db_engine()
    yield
    await close_db_engine()


app = FastAPI(title="Boilerplate FAST API", lifespan=lifespan)

setup_exception_handlers(app)
app.add_middleware(UnifiedResponseMiddleware)

app.include_router(user_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/error")
async def error_root():
    raise Exception("serious error occurred")
