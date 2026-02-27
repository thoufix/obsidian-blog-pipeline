import re
import shutil
from pathlib import Path
from urllib.parse import unquote

CONTENT_DIR = Path("hugo-site/content/posts")

def normalize_filename(name):
    name = unquote(name)  # decode %20
    name = name.replace(" ", "-")
    return name.lower()

def process_markdown(md_path):
    text = md_path.read_text(encoding="utf-8")
    updated = False

    # Handle Obsidian style ![[image.png]]
    obsidian_matches = re.findall(r'!\[\[([^\]]+)\]\]', text)

    for image in obsidian_matches:
        decoded = unquote(image)
        image_path = md_path.parent / decoded

        if not image_path.exists():
            continue

        new_name = normalize_filename(decoded)
        new_path = md_path.parent / new_name

        if image_path != new_path:
            shutil.move(image_path, new_path)

        text = text.replace(f"![[{image}]]", f"![]({new_name})")
        updated = True

    # Handle Markdown style ![](image.png)
    md_matches = re.findall(r'!\[[^\]]*\]\(([^)]+)\)', text)

    for image in md_matches:
        decoded = unquote(image)
        image_path = md_path.parent / decoded

        if image_path.exists():
            new_name = normalize_filename(decoded)
            new_path = md_path.parent / new_name

            if image_path != new_path:
                shutil.move(image_path, new_path)

            text = text.replace(image, new_name)
            updated = True

    if updated:
        md_path.write_text(text, encoding="utf-8")

for md_file in CONTENT_DIR.rglob("*.md"):
    process_markdown(md_file)

print("Image normalization complete.")