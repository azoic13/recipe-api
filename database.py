import os
from supabase import create_client
from dotenv import load_dotenv

# Only load .env file locally, Railway provides vars directly
load_dotenv()

# Get variables
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")

# Debug
print(f"SUPABASE_URL loaded: {supabase_url}")
print(f"SUPABASE_KEY loaded: {supabase_key is not None}")

if not supabase_url or not supabase_key:
    raise ValueError("Missing SUPABASE_URL or SUPABASE_KEY environment variables")

# Connect to Supabase
supabase = create_client(supabase_url, supabase_key)

# ─────────────────────────────
# Save a recipe to the database
# ─────────────────────────────
def save_recipe(recipe: dict, source_url: str = None) -> dict:
    data = {
        "title": recipe["title"],
        "ingredients": recipe["ingredients"],
        "steps": recipe["steps"],
        "source_url": source_url or ""
    }
    result = supabase.table("recipes").insert(data).execute()
    return result.data[0]

# ─────────────────────────────
# Get all saved recipes
# ─────────────────────────────
def get_all_recipes() -> list:
    result = supabase.table("recipes") \
        .select("*") \
        .order("created_at", desc=True) \
        .execute()
    return result.data
# ─────────────────────────────
# Delete a recipe by ID
# ─────────────────────────────
def delete_recipe(recipe_id: str) -> dict:
    result = supabase.table("recipes") \
        .delete() \
        .eq("id", recipe_id) \
        .execute()
    return {"deleted": True}