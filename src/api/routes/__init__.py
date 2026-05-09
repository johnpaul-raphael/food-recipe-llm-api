from fastapi import HTTPException
from src.api.schemas import RecipeRequest
from src.api.schemas import RecipeResponse
from fastapi import APIRouter
from src.model.inference import RecipeGenerator

generate = RecipeGenerator()
router = APIRouter()

@router.get("/health")
def health_check():
    return {"status": "ok"}

@router.post("/generate")
def generate_recipe(request: RecipeRequest):
    try:
       result = generate.generate_recipe(request.prompt)
       return RecipeResponse(prompt=request.prompt, generated_recipe=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
