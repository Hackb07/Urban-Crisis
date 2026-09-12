import os
import re

def remove_all_non_ascii(text):
    # This removes all characters that are not in the standard ASCII range (0-127)
    return re.sub(r'[^\x00-\x7F]+', '', text)

def clean_project():
    root_dir = '.'
    ignore_dirs = {'.venv', '.git', '__pycache__'}

    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]

        for file in files:
            if file.endswith(('.py', '.md', '.ms', '.txt')):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    cleaned_content = remove_all_non_ascii(content)

                    if cleaned_content != content:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(cleaned_content)
                        print(f"Cleaned: {file_path}")
                except Exception as e:
                    print(f"Error cleaning {file_path}: {e}")

if __name__ == "__main__":
    clean_project()
