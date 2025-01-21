import os

def generate_table_of_contents(root_dir, target_dir=None):
    toc = "# Table of Contents\n\n"
    
    def add_entry(section, file_name, relative_path):
        # link_path = relative_path.replace('.md', '')
        # return f"- [{file_name}]({link_path})\n"

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