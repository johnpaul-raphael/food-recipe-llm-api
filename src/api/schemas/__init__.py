from pydantic import BaseModel, Field
from typing import List


class RecipeRequest(BaseModel):
    prompt: str = Field(..., min_length=3, max_length=100, examples=["chicken biryani"])


class RecipeResponse(BaseModel):
    prompt: str
    title: str
    ingredients: List[str]
    instructions: List[str]
