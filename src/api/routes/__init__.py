from fastapi import HTTPException, APIRouter
from src.api.schemas import RecipeRequest, RecipeResponse
from src.model.inference import RecipeGenerator
from src.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()
generate = RecipeGenerator()


@router.get("/health")
def health_check():
    logger.info("Health check requested")
    return {"status": "ok"}


@router.post("/generate", response_model=RecipeResponse)
def generate_recipe(request: RecipeRequest):
    logger.info(f"Recipe request received — prompt: '{request.prompt}'")
    try:
        result = generate.generate_recipe(request.prompt)
        logger.info("Recipe returned to client successfully")
        return RecipeResponse(
            prompt=request.prompt,
            title=result["title"],
            ingredients=result["ingredients"],
            instructions=result["instructions"]
        )
    except Exception as e:
        logger.error(f"Error generating recipe: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
