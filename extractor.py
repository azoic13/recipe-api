import yt_dlp
import anthropic
import json
import os
from dotenv import load_dotenv

load_dotenv()


# ─────────────────────────────────────
# STEP A: Get caption from Instagram URL
# ─────────────────────────────────────
def get_instagram_caption(url: str) -> str:
    options = {
        'quiet': True,
        'skip_download': True,
        'no_warnings': True,
        # Pretend to be a browser to avoid blocks
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
    }

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=False)
            caption = info.get('description', '')
            title = info.get('title', '')

            # Combine title and caption for better extraction
            full_text = f"{title}\n{caption}".strip()
            return full_text
    except Exception as e:
        print(f"yt-dlp error: {e}")
        return ""


# ─────────────────────────────────────
# STEP B: Send text to Claude → get recipe JSON
# ─────────────────────────────────────
def extract_recipe_with_ai(text: str) -> dict:
    client = anthropic.Anthropic(
        api_key=os.environ.get("ANTHROPIC_API_KEY")
    )

    prompt = f"""
    Extract a recipe from the text below.
    Return ONLY valid JSON. No extra text, no explanation, no markdown.

    Use this exact format:
    {{
      "title": "Recipe name here",
      "ingredients": [
        {{"name": "flour", "quantity": "2", "unit": "cups"}},
        {{"name": "egg", "quantity": "1", "unit": ""}}
      ],
      "steps": [
        "Step 1: Do this...",
        "Step 2: Then do this..."
      ]
    }}

    If you cannot find a recipe in the text, return:
    {{"error": "No recipe found in this content"}}

    Text to extract from:
    {text}
    """

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    raw_text = message.content[0].text

    # Clean markdown fences if present
    clean_text = raw_text.strip()
    if clean_text.startswith('```'):
        clean_text = clean_text.split('```')[1]
        if clean_text.startswith('json'):
            clean_text = clean_text[4:]

    recipe = json.loads(clean_text.strip())
    return recipe


# ─────────────────────────────────────
# STEP C: Extract from URL
# ─────────────────────────────────────
def extract_recipe_from_url(url: str) -> dict:
    print(f"Getting content from: {url}")
    caption = get_instagram_caption(url)

    if not caption:
        return {
            "error": "Could not get content from this URL. Try pasting the caption text instead."
        }

    print(f"Content found: {caption[:100]}...")
    recipe = extract_recipe_with_ai(caption)
    return recipe


# ─────────────────────────────────────
# STEP D: Extract from pasted text
# ─────────────────────────────────────
def extract_recipe_from_text(text: str) -> dict:
    print("Extracting from pasted text...")
    recipe = extract_recipe_with_ai(text)
    return recipe