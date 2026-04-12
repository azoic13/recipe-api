import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")

supabase = create_client(supabase_url, supabase_key)


# ─────────────────────────────
# RECIPES
# ─────────────────────────────

def save_recipe(recipe: dict, source_url: str = None, cookbook_id: str = None) -> dict:
    data = {
        "title": recipe["title"],
        "ingredients": recipe["ingredients"],
        "steps": recipe["steps"],
        "source_url": source_url or "",
        "cookbook_id": cookbook_id
    }
    result = supabase.table("recipes").insert(data).execute()
    return result.data[0]

def get_all_recipes() -> list:
    result = supabase.table("recipes") \
        .select("*") \
        .order("created_at", desc=True) \
        .execute()
    return result.data

def get_recipes_by_cookbook(cookbook_id: str) -> list:
    result = supabase.table("recipes") \
        .select("*") \
        .eq("cookbook_id", cookbook_id) \
        .order("created_at", desc=True) \
        .execute()
    return result.data

def delete_recipe(recipe_id: str) -> dict:
    supabase.table("recipes") \
        .delete() \
        .eq("id", recipe_id) \
        .execute()
    return {"deleted": True}


# ─────────────────────────────
# COOKBOOKS
# ─────────────────────────────

def get_all_cookbooks() -> list:
    result = supabase.table("cookbooks") \
        .select("*") \
        .order("created_at", desc=True) \
        .execute()
    return result.data

def create_cookbook(name: str) -> dict:
    result = supabase.table("cookbooks") \
        .insert({"name": name}) \
        .execute()
    return result.data[0]

def delete_cookbook(cookbook_id: str) -> dict:
    supabase.table("cookbooks") \
        .delete() \
        .eq("id", cookbook_id) \
        .execute()
    return {"deleted": True}