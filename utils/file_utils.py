import os
import markdown2

def clear_temp_clipboard(temp_clipboard_dir):
    prompt = input("Do you want to clear the files inside the 'temp_clipboard' folder? (y/N): ").strip().lower()
    if prompt == 'y':
        for file in os.listdir(temp_clipboard_dir):
            file_path = os.path.join(temp_clipboard_dir, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        with open(os.path.join(temp_clipboard_dir, "clipboard.md"), 'w') as clipboard_file:
            clipboard_file.write("# Clipboard\n\n")

def convert_readme_to_html(readme_path, html_path):
    with open(readme_path, 'r') as readme_file:
        readme_content = readme_file.read()
    
    html_content = markdown2.markdown(readme_content)
    
    with open(html_path, 'w') as html_file:
        html_file.write(html_content)