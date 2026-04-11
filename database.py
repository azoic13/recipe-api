import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

# Connect to Supabase
supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

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