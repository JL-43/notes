import os
from PIL import Image

def convert_images(root_dir):
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith((".png", ".jpg", ".jpeg")):
                original_path = os.path.join(subdir, file)
                webp_path = os.path.splitext(original_path)[0] + ".webp"
                
                # Check if the WebP file already exists
                if os.path.exists(webp_path):
                    continue
                
                # Convert to WebP format
                with Image.open(original_path) as img:
                    img = img.convert("RGB")
                    img.save(webp_path, "webp")
                
                # remove the original file
                os.remove(original_path)