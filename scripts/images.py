import re
import shutil
from pathlib import Path

CONTENT_DIR = Path("content")

def normalize_filename(name):
    name = name.replace("%20", " ")
    name = name.replace(" ", "-")
    return name.lower()

def process_markdown(md_path):
    text = md_path.read_text(encoding="utf-8")
    updated = False

    # Handle Obsidian style ![[image.png]]
    obsidian_matches = re.findall(r'!\[\[([^\]]+)\]\]', text)

    for image in obsidian_matches:
        image_path = md_path.parent / image

        if not image_path.exists():
            continue

        new_name = normalize_filename(image_path.name)
        new_path = md_path.parent / new_name

        if image_path != new_path:
            shutil.move(image_path, new_path)

        text = text.replace(f"![[{image}]]", f"![]({new_name})")
        updated = True

    # Handle Markdown style ![](image.png)
    md_matches = re.findall(r'!\[[^\]]*\]\(([^)]+)\)', text)

    for image in md_matches:
        image_path = md_path.parent / image

        if image_path.exists():
            new_name = normalize_filename(image_path.name)
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
