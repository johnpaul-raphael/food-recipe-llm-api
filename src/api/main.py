from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
from mangum import Mangum
from src.api.routes import router
from src.utils.logger import get_logger

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application startup — model loading initiated")
    yield
    logger.info("Application shutdown — cleanup complete")


app = FastAPI(
    title="Food Recipe LLM API",
    description="Generate recipes based on the prompt",
    version="1.0.0",
    lifespan=lifespan
)

app.mount("/static", StaticFiles(directory="src/api/static"), name="static")
app.include_router(router, prefix="/api")


@app.get("/")
def root():
    logger.info("Root endpoint accessed — serving UI")
    return FileResponse("src/api/static/index.html")


handler = Mangum(app)
