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
    bundle_dir = md_path.parent
    attachments_dir = bundle_dir / "attachments"

    # First, move all images from attachments/ to bundle root
    if attachments_dir.exists():
        for img_file in attachments_dir.iterdir():
            if img_file.suffix.lower() in ['.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg']:
                # Normalize filename
                new_name = normalize_filename(img_file.name)
                new_path = bundle_dir / new_name
                
                # Move to bundle root
                shutil.move(str(img_file), str(new_path))
                print(f"  Moved: attachments/{img_file.name} -> {new_name}")
        
        # Remove empty attachments folder
        try:
            attachments_dir.rmdir()
            print(f"  Removed: attachments/")
        except:
            pass
    
    # Handle Obsidian style ![[image.png]]
    obsidian_matches = re.findall(r'!\[\[([^\]]+)\]\]', text)

    for image in obsidian_matches:
        decoded = unquote(image)
        # Check both bundle root and attachments
        image_path = bundle_dir / decoded
        if not image_path.exists() and attachments_dir.exists():
            image_path = attachments_dir / decoded

        if not image_path.exists():
            continue

        new_name = normalize_filename(decoded)
        new_path = bundle_dir / new_name

        if image_path != new_path:
            shutil.move(image_path, new_path)

        text = text.replace(f"![[{image}]]", f"![]({new_name})")
        updated = True

    # Handle Markdown style ![](image.png) - including attachments/ path
    md_matches = re.findall(r'!\[[^\]]*\]\(([^)]+)\)', text)

    for image in md_matches:
        decoded = unquote(image)
        
        # Remove attachments/ prefix if present
        if decoded.startswith('attachments/'):
            decoded = decoded.replace('attachments/', '')
            text = text.replace(image, decoded)
            updated = True
        
        image_path = bundle_dir / decoded

        if image_path.exists():
            new_name = normalize_filename(decoded)
            new_path = bundle_dir / new_name

            if image_path != new_path:
                shutil.move(image_path, new_path)

            if image != new_name:
                text = text.replace(image, new_name)
                updated = True

    if updated:
        md_path.write_text(text, encoding="utf-8")

for md_file in CONTENT_DIR.rglob("*.md"):
    process_markdown(md_file)

print("Image normalization complete.")
