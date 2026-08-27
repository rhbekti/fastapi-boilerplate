from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.core.dependencies import engine
from src.core.exceptions import setup_exception_handlers
from src.core.logging import setup_logging
from src.core.middlewares import UnifiedResponseMiddleware
from src.user.router import router as user_router

setup_logging()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Create Lifespan"""
    yield
    await engine.dispose()


app = FastAPI(title="Boilerplate FAST API", lifespan=lifespan)

setup_exception_handlers(app)
app.add_middleware(UnifiedResponseMiddleware)

app.include_router(user_router)


@app.get("/")
async def root():
    """Root Path"""
    return {"message": "Hello World"}


@app.get("/error")
async def error_root():
    """Error Root"""
    raise Exception("serious error occurred")
