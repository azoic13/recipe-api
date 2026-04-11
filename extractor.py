import yt_dlp
import anthropic
import json
import os
from dotenv import load_dotenv

load_dotenv()  # reads your .env file

# ─────────────────────────────────────
# STEP A: Get caption from Instagram URL
# ─────────────────────────────────────
def get_instagram_caption(url: str) -> str:
    options = {
        'quiet': True,           # don't print download logs
        'skip_download': True,   # we only want the caption, not the video
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=False)
        caption = info.get('description', '')
        return caption


# ─────────────────────────────────────
# STEP B: Send caption to Claude → get recipe JSON
# ─────────────────────────────────────
def extract_recipe_with_ai(caption: str) -> dict:
    client = anthropic.Anthropic(
        api_key=os.getenv("ANTHROPIC_API_KEY")
    )

    prompt = f"""
    Extract a recipe from the text below.
    Return ONLY valid JSON. No extra text, no explanation.

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

    Text to extract from:
    {caption}
    """

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

# Get the text Claude returned
    raw_text = message.content[0].text

    # Remove markdown code fences if Claude added them
    clean_text = raw_text.strip()
    if clean_text.startswith('```'):
        clean_text = clean_text.split('```')[1]
        if clean_text.startswith('json'):
            clean_text = clean_text[4:]

    # Convert text to a Python dictionary
    recipe = json.loads(clean_text.strip())
    return recipe


# ─────────────────────────────────────
# STEP C: The main function — combines A + B
# ─────────────────────────────────────
def extract_recipe_from_url(url: str) -> dict:
    print(f"Getting caption from: {url}")
    caption = get_instagram_caption(url)

    if not caption:
        return {"error": "Could not find any text in this post"}

    print("Caption found! Sending to Claude...")
    recipe = extract_recipe_with_ai(caption)
    return recipe


# ─────────────────────────────────────
# BONUS: Also works if user pastes text directly
# ─────────────────────────────────────
def extract_recipe_from_text(text: str) -> dict:
    print("Extracting recipe from pasted text...")
    recipe = extract_recipe_with_ai(text)
    return recipe
