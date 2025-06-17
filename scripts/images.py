import os
import re
import shutil

# Paths (using raw strings to handle Windows backslashes correctly)
posts_dir = r"C:\Users\AI\Documents\Obsidian Vault\posts"  # Your Markdown files directory
attachments_dir = r"C:\Users\AI\Documents\Obsidian Vault"  # Your Obsidian vault directory where images are stored
static_images_dir = r"C:\Users\AI\Documents\chuckblog\static\images"  # Hugo static images directory

# Ensure the static_images_dir exists
os.makedirs(static_images_dir, exist_ok=True)

# Step 1: Process each markdown file in the posts directory
for filename in os.listdir(posts_dir):
    if filename.endswith(".md"):
        filepath = os.path.join(posts_dir, filename)
        
        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()
        
        # Step 2: Find all image links in the format [[image_name.png]]
        images = re.findall(r'\[\[([^]]*\.png|jpe?g)\]\]', content)
        
        # Step 3: Replace image links and ensure URLs are correctly formatted
        for image in images:
            # Prepare the Markdown-compatible link
            markdown_image = f"![Image Description](/images/{image.replace(' ', '%20')})"
            content = content.replace(f"[[{image}]]", markdown_image)
            
            # Step 4: Copy the image to the Hugo static/images directory if it exists
            image_source = os.path.join(attachments_dir, image)
            if os.path.exists(image_source):
                shutil.copy(image_source, static_images_dir)
                print(f"Copied: {image} to {static_images_dir}")
            else:
                print(f"Image not found: {image_source}")

        # Step 5: Write the updated content back to the markdown file
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(content)

print("Markdown files processed and images copied successfully.")
