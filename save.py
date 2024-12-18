import os
from utils.toc_utils import generate_table_of_contents, update_readme, update_personal_toc
from utils.image_utils import convert_images
from utils.git_utils import auto_commit
from utils.file_utils import clear_temp_clipboard, convert_readme_to_html

if __name__ == "__main__":
    root_dir = os.path.dirname(os.path.abspath(__file__))

    # Generate ToC for the entire project
    personal_toc = generate_table_of_contents(root_dir)
    update_personal_toc(os.path.join(root_dir, 'personal_toc.md'), personal_toc)

    # Generate ToC for the public folder
    public_toc = generate_table_of_contents(root_dir, target_dir='public')
    update_readme(os.path.join(root_dir, 'README.md'), public_toc)
    
    # Convert README.md to index.html
    convert_readme_to_html(os.path.join(root_dir, 'README.md'), os.path.join(root_dir, 'index.html'))

    temp_clipboard_directory = os.path.join(root_dir, "temp_clipboard")
    if os.path.exists(temp_clipboard_directory):
        clear_temp_clipboard(temp_clipboard_directory)
    
    convert_images(root_dir)
    
    auto_commit(root_dir)