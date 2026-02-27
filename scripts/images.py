import os
import re
import shutil
from urllib.parse import quote

def get_platform_config():
    """Return OS-specific configuration"""
    if os.name == 'nt':  # Windows
        return {
            'posts_dir': r"D:\Sandbox\Dev\obsidian-blog-pipeline\hugo-site\content\posts",
            'attachments_dir': r"D:\Sandbox\Dev\obsidian-blog-pipeline\hugo-site\content\posts",
            'static_images_dir': r"D:\Sandbox\Dev\obsidian-blog-pipeline\hugo-site\static\images",
            'newline': '\r\n'  # Windows line endings
        }
    else:  # Linux (Raspberry Pi)
        return {
            'posts_dir': "/home/pi/obsidian-blog-pipeline/hugo-site/content/posts",
            'attachments_dir': "/home/pi/obsidian-blog-pipeline/hugo-site/content/posts",
            'static_images_dir': "/home/pi/obsidian-blog-pipeline/hugo-site/static/images",
            'newline': '\n'
        }

def process_images():
    config = get_platform_config()
    os.makedirs(config['static_images_dir'], exist_ok=True)

    print(f"Running on: {'Windows' if os.name == 'nt' else 'Raspberry Pi'}")
    print(f"Processing markdown files in: {config['posts_dir']}")
    print(f"Image source directory: {config['attachments_dir']}")
    print(f"Target image directory: {config['static_images_dir']}")
    print("-" * 50)

    processed_files = 0
    total_images = 0
    image_patterns = [
        (r'!\[\[([^\]]+\.(?:png|jpg|jpeg|gif|webp|svg))\]\]', 'obsidian'),
        (r'!\[[^\]]*\]\(([^\)]+\.(?:png|jpg|jpeg|gif|webp|svg))\)', 'markdown')
    ]

    for filename in os.listdir(config['posts_dir']):
        if not filename.endswith(".md"):
            continue

        filepath = os.path.join(config['posts_dir'], filename)
        print(f"\nProcessing: {filename}")

        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()

        changes_made = False

        for pattern, pattern_type in image_patterns:
            for match in re.finditer(pattern, content, re.IGNORECASE):
                image = match.group(1)
                print(f"  Found {pattern_type} image reference: {image}")

                if pattern_type == 'markdown':
                    image = os.path.basename(image)

                encoded_image = quote(image)
                hugo_image = f"![{image}](/images/{encoded_image})"

                if pattern_type == 'obsidian':
                    content = content.replace(f"![[{image}]]", hugo_image)
                else:
                    content = re.sub(
                        r'!\[[^\]]*\]\(' + re.escape(image) + r'\)',
                        hugo_image,
                        content
                    )

                image_source = os.path.join(config['attachments_dir'], image)
                image_dest = os.path.join(config['static_images_dir'], image)

                if os.path.exists(image_source):
                    try:
                        shutil.copy2(image_source, image_dest)
                        print(f"    [OK] Copied: {image}")
                        total_images += 1
                        changes_made = True
                    except Exception as e:
                        print(f"    [ERR] Error copying {image}: {str(e)}")
                else:
                    print(f"    [ERR] Image not found: {image_source}")

        if changes_made:
            with open(filepath, "w", encoding="utf-8", newline=config['newline']) as file:
                file.write(content)
            print(f"  [OK] Updated markdown file")
            processed_files += 1
        else:
            print("  No image changes needed")

    print("\n" + "-" * 50)
    print("Processing complete!")
    print(f"Markdown files processed: {processed_files}")
    print(f"Images copied: {total_images}")
    print("\nNext steps:")
    print("1. Run 'git status' to see changes")
    print("2. Commit and push to GitHub")
    print("3. GitHub Actions will deploy to https://blog.pilab.space")

if __name__ == "__main__":
    process_images()
