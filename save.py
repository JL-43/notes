import os
import subprocess
from datetime import datetime
from utils.toc_utils import generate_table_of_contents, update_readme, update_personal_toc
from utils.image_utils import convert_images
from utils.git_utils import auto_commit
from utils.file_utils import clear_temp_clipboard, convert_readme_to_html

def generate_tailwind_css():
    try:
        subprocess.run([
            "npx", 
            "tailwindcss", 
            "-i", 
            "./assets/css/input.css", 
            "-o", 
            "./assets/css/style.css", 
            "--minify"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error generating Tailwind CSS: {e}")
        return False
    return True

if __name__ == "__main__":
    root_dir = os.path.dirname(os.path.abspath(__file__))

    # Ensure directories exist
    os.makedirs('blog', exist_ok=True)
    os.makedirs('assets/css', exist_ok=True)

    # Generate ToC for the entire project
    personal_toc = generate_table_of_contents(root_dir)
    update_personal_toc(os.path.join(root_dir, 'bogart.md'), personal_toc)

    # Generate ToC for the blog
    blog_toc = generate_table_of_contents(root_dir, target_dir='blog')
    latest_article_path = os.path.join(root_dir, 'blog', 'latest_article.md')
    readme_path = os.path.join(root_dir, 'README.md')
    update_readme(readme_path, blog_toc, latest_article_path)

    # Generate Tailwind CSS and convert to HTML
    if generate_tailwind_css():
        convert_readme_to_html(readme_path, os.path.join(root_dir, 'index.html'))
    
    temp_clipboard_directory = os.path.join(root_dir, "temp_clipboard")
    if os.path.exists(temp_clipboard_directory):
        clear_temp_clipboard(temp_clipboard_directory)
    
    convert_images(root_dir)
    auto_commit(root_dir)