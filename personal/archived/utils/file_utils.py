import os
import markdown2
from datetime import datetime

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
    
    html_content = markdown2.markdown(readme_content, extras=['tables'])
    
    html_template = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link href="assets/css/style.css" rel="stylesheet">
            <title>JL's Notes</title>
        </head>
        <body class="bg-gray-100">
            <div class="container mx-auto px-4 py-8">
                <header class="mb-8 bg-white shadow-lg rounded-lg p-6">
                    <h1 class="text-4xl font-bold text-gray-800">JL's Notes</h1>
                    <nav class="mt-4">
                        <a href="#latest-article" class="text-blue-600 hover:text-blue-800 mr-4">Latest Article</a>
                        <a href="#table-of-contents" class="text-blue-600 hover:text-blue-800">Table of Contents</a>
                    </nav>
                </header>
                <main class="prose prose-lg max-w-none bg-white shadow-lg rounded-lg p-8">
                    {html_content}
                </main>
            </div>
        </body>
        </html>
    """
    
    with open(html_path, 'w') as html_file:
        html_file.write(html_template)