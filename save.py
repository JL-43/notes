import os
import subprocess
from datetime import datetime
from PIL import Image
import json
import markdown2

def generate_table_of_contents(root_dir, target_dir=None):
    toc = "# Table of Contents\n\n"
    
    def add_entry(section, file_name, relative_path):
        return f"- [{file_name}]({relative_path})\n"
    
    sections_dict = {}
    
    for subdir, _, files in os.walk(root_dir):
        if "temp_clipboard" in subdir:
            continue
        for file in files:
            if file.endswith(".md") and file != "README.md":
                relative_path = os.path.relpath(os.path.join(subdir, file), root_dir)
                if target_dir and not relative_path.startswith(target_dir):
                    continue
                sections = relative_path.split(os.sep)
                file_name = os.path.splitext(sections[-1])[0]
                section = " / ".join(sections[:-1])
                
                if section not in sections_dict:
                    sections_dict[section] = []
                sections_dict[section].append((file_name, relative_path))
    
    for section, entries in sections_dict.items():
        if section:
            toc += f"## {section}\n"
        for file_name, relative_path in entries:
            toc += add_entry(section, file_name, relative_path)
    
    return toc

def update_readme(readme_path, toc, latest_article_path):
    with open(readme_path, 'w') as readme_file:
        readme_file.write("# Latest Article\n\n")
        
        if os.path.exists(latest_article_path):
            print(f"Adding the latest article to the README file: {latest_article_path}")
            with open(latest_article_path, 'r') as article_file:
                readme_file.write(article_file.read())
                readme_file.write("\n\n")
        else:
            print("No latest article found.")
        
        readme_file.write(toc)

def update_personal_toc(toc_path, toc):
    with open(toc_path, 'w') as toc_file:
        toc_file.write("# Personal Table of Contents\n\n")
        toc_file.write(toc)

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

def clear_temp_clipboard(temp_clipboard_dir):
    prompt = input("Do you want to clear the files inside the 'temp_clipboard' folder? (y/N): ").strip().lower()
    if prompt == 'y':
        for file in os.listdir(temp_clipboard_dir):
            file_path = os.path.join(temp_clipboard_dir, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        with open(os.path.join(temp_clipboard_dir, "clipboard.md"), 'w') as clipboard_file:
            clipboard_file.write("# Clipboard\n\n")

def auto_commit(script_dir):
    os.chdir(script_dir)
    
    # Check if there are any changes before proceeding
    if not subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True).stdout.strip():
        print("No changes to commit. Exiting.")
        return
    
    # Add, commit, and push changes
    subprocess.run(["git", "add", "."])
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    commit_message = f"auto-commit on {timestamp}"
    if subprocess.run(["git", "commit", "-m", commit_message]).returncode == 0:
        subprocess.run(["git", "push"])

def convert_readme_to_html(readme_path, html_path):
    with open(readme_path, 'r') as readme_file:
        readme_content = readme_file.read()
    
    html_content = markdown2.markdown(readme_content)
    
    with open(html_path, 'w') as html_file:
        html_file.write(html_content)

if __name__ == "__main__":
    root_dir = os.path.dirname(os.path.abspath(__file__))

    # Generate ToC for the entire project
    personal_toc = generate_table_of_contents(root_dir)
    update_personal_toc(os.path.join(root_dir, 'bogart.md'), personal_toc)

    # Generate ToC for the blog folder
    blog_toc = generate_table_of_contents(root_dir, target_dir='blog')
    latest_article_path = os.path.join(root_dir, 'blog', 'latest_article.md')
    readme_path = os.path.join(root_dir, 'README.md')
    update_readme(os.path.join(root_dir, 'README.md'), blog_toc, latest_article_path)
    
    # Convert README.md to index.html
    convert_readme_to_html(readme_path, os.path.join(root_dir, 'index.html'))

    temp_clipboard_directory = os.path.join(root_dir, "temp_clipboard")
    if os.path.exists(temp_clipboard_directory):
        clear_temp_clipboard(temp_clipboard_directory)
    
    convert_images(root_dir)
    
    auto_commit(root_dir)