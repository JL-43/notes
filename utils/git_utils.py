import os
import subprocess
from datetime import datetime

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