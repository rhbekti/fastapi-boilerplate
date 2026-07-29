from fastapi import FastAPI
from src.user.router import router as user_router

app = FastAPI(title="Boilerplate FAST API")

app.include_router(user_router)


@app.get("/")
def root():
    return {"message": "API RUNNING"}
