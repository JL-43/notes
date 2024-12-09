import os
import subprocess
from datetime import datetime

def generate_table_of_contents(root_dir):
    toc = "| Section        | File Name                          |\n"
    toc += "|----------------|------------------------------------|\n"
    
    for subdir, _, files in os.walk(root_dir):
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
    else:
        print("No changes to commit.")

def clear_temp_clipboard(temp_clipboard_dir):
    prompt = input("Do you want to clear the files inside the 'temp_clipboard' folder? (y/N): ").strip().lower()
    if prompt == 'y':
        for file in os.listdir(temp_clipboard_dir):
            file_path = os.path.join(temp_clipboard_dir, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        with open(os.path.join(temp_clipboard_dir, "clipboard.md"), 'w') as clipboard_file:
            clipboard_file.write("# Clipboard\n\n")

if __name__ == "__main__":
    root_directory = "."  # Set to your workspace root directory
    readme_file_path = os.path.join(root_directory, "README.md")
    
    # Generate and update the table of contents
    table_of_contents = generate_table_of_contents(root_directory)
    update_readme(readme_file_path, table_of_contents)
    
    # Clear temp_clipboard folder if prompted
    temp_clipboard_directory = os.path.join(root_directory, "temp_clipboard")
    if os.path.exists(temp_clipboard_directory):
        clear_temp_clipboard(temp_clipboard_directory)
    
    # Perform auto-commit actions
    script_directory = os.path.dirname(os.path.abspath(__file__))
    auto_commit(script_directory)