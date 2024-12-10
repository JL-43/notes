import os
import subprocess
from datetime import datetime
from PIL import Image
import json

PROCESSED_FILES_PATH = os.path.join('utils', 'processed_files.json')

# def load_processed_files():
#     if os.path.exists(PROCESSED_FILES_PATH):
#         with open(PROCESSED_FILES_PATH, 'r') as file:
#             return json.load(file)
#     return []

# def save_processed_files(processed_files):
#     os.makedirs('utils', exist_ok=True)
#     with open(PROCESSED_FILES_PATH, 'w') as file:
#         json.dump(processed_files, file)

# def rename_files_with_whitespaces(root_dir):
#     processed_files = load_processed_files()
#     updated_files = set(processed_files)
#     for subdir, _, files in os.walk(root_dir):
#         for file in files:
#             if ' ' in file and file not in processed_files:
#                 old_path = os.path.join(subdir, file)
#                 new_file = file.replace(' ', '_')
#                 new_path = os.path.join(subdir, new_file)
#                 os.rename(old_path, new_path)
#                 processed_files.append(new_file)
#     save_processed_files(processed_files)

def generate_table_of_contents(root_dir):
    toc = "| Section        | File Name                          |\n"
    toc += "|----------------|------------------------------------|\n"
    
    for subdir, _, files in os.walk(root_dir):
        if "temp_clipboard" in subdir:
            continue
        for file in files:
            if file.endswith(".md") and file != "README.md":
                relative_path = os.path.relpath(os.path.join(subdir, file), root_dir)
                sections = relative_path.split(os.sep)
                file_name = os.path.splitext(sections[-1])[0]
                section = " > ".join(sections[:-1])
                toc += f"| {section} | [{file_name}]({relative_path}) |\n"
    
    return toc

def update_readme(readme_path, toc):
    with open(readme_path, 'w') as readme_file:
        readme_file.write("# JL's notes\n\n## Table of Contents\n\n")
        readme_file.write(toc)

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

if __name__ == "__main__":
    root_dir = os.path.dirname(os.path.abspath(__file__))

    # rename_files_with_whitespaces(root_dir)

    toc = generate_table_of_contents(root_dir)
    
    temp_clipboard_directory = os.path.join(root_dir, "temp_clipboard")
    if os.path.exists(temp_clipboard_directory):
        clear_temp_clipboard(temp_clipboard_directory)
    
    update_readme(os.path.join(root_dir, 'README.md'), toc)
    
    convert_images(root_dir)
    
    auto_commit(root_dir)