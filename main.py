from fastapi import FastAPI
from pydantic import BaseModel
from extractor import extract_recipe_from_url, extract_recipe_from_text
from database import save_recipe, get_all_recipes

app = FastAPI()

class UrlInput(BaseModel):
    url: str

class TextInput(BaseModel):
    text: str


# ─────────────────────────────
# Health check
# ─────────────────────────────
@app.get("/")
def home():
    return {"message": "Recipe API is running ✅"}


# ─────────────────────────────
# Get all saved recipes
# ─────────────────────────────
@app.get("/recipes")
def list_recipes():
    recipes = get_all_recipes()
    return recipes


# ─────────────────────────────
# Extract from URL + save
# ─────────────────────────────
@app.post("/extract-from-url")
def extract_from_url(data: UrlInput):
    recipe = extract_recipe_from_url(data.url)

    # If error, return it without saving
    if "error" in recipe:
        return recipe

    saved = save_recipe(recipe, source_url=data.url)
    return saved


# ─────────────────────────────
# Extract from text + save
# ─────────────────────────────
@app.post("/extract-from-text")
def extract_from_text(data: TextInput):
    recipe = extract_recipe_from_text(data.text)

    # If error, return it without saving
    if "error" in recipe:
        return recipe

    saved = save_recipe(recipe)
    return saved