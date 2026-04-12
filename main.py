from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from extractor import extract_recipe_from_url, extract_recipe_from_text
from database import (
    save_recipe, get_all_recipes, get_recipes_by_cookbook,
    delete_recipe, get_all_cookbooks, create_cookbook, 
    delete_cookbook, move_recipe_to_cookbook
)

app = FastAPI()

class UrlInput(BaseModel):
    url: str
    cookbook_id: Optional[str] = None

class TextInput(BaseModel):
    text: str
    cookbook_id: Optional[str] = None

class CookbookInput(BaseModel):
    name: str


# ─────────────────────────────
# Health check
# ─────────────────────────────
@app.get("/")
def home():
    return {"message": "Recipe API is running ✅"}


# ─────────────────────────────
# Recipes
# ─────────────────────────────
@app.get("/recipes")
def list_recipes():
    return get_all_recipes()

@app.get("/recipes/cookbook/{cookbook_id}")
def list_recipes_by_cookbook(cookbook_id: str):
    return get_recipes_by_cookbook(cookbook_id)

@app.post("/extract-from-url")
def extract_from_url(data: UrlInput):
    recipe = extract_recipe_from_url(data.url)
    if "error" in recipe:
        return recipe
    return save_recipe(recipe, source_url=data.url, cookbook_id=data.cookbook_id)

@app.post("/extract-from-text")
def extract_from_text(data: TextInput):
    recipe = extract_recipe_from_text(data.text)
    if "error" in recipe:
        return recipe
    return save_recipe(recipe, cookbook_id=data.cookbook_id)

@app.delete("/recipes/{recipe_id}")
def remove_recipe(recipe_id: str):
    return delete_recipe(recipe_id)


# ─────────────────────────────
# Cookbooks
# ─────────────────────────────
@app.get("/cookbooks")
def list_cookbooks():
    return get_all_cookbooks()

@app.post("/cookbooks")
def add_cookbook(data: CookbookInput):
    return create_cookbook(data.name)

@app.delete("/cookbooks/{cookbook_id}")
def remove_cookbook(cookbook_id: str):
    return delete_cookbook(cookbook_id)
class MoveRecipeInput(BaseModel):
    cookbook_id: Optional[str] = None

@app.patch("/recipes/{recipe_id}/move")
def move_recipe(recipe_id: str, data: MoveRecipeInput):
    return move_recipe_to_cookbook(recipe_id, data.cookbook_id)