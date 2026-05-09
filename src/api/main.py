from fastapi import FastAPI
from src.api.routes import router
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application startup")
    yield
    print("Application shutdown")

app = FastAPI(title="Recipe Generator API",
description="Generate recipes based on the prompt",
version="1.0.0",
lifespan=lifespan)

app.include_router(router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Welcome to the Recipe Generator API"}