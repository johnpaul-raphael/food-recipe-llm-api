from pydantic import Field
from pydantic import BaseModel

class RecipeRequest(BaseModel):
    prompt: str = Field(...,
    min_length=3,
    max_length=100,
    examples=["chicken briyani"])

class RecipeResponse(BaseModel):
    prompt: str
    generated_recipe: str