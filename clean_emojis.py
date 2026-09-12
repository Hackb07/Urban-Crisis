import os
import re

def remove_emojis(text):
    # Regex to match most emojis and symbols
    # This targets common emoji ranges and non-ASCII symbols
    emoji_pattern = re.compile(
        u'['
        u'\U00010000-\U0010ffff'  # Supplemental Planes (Emojis)
        u'-'            # Miscellaneous Symbols and Dingbats
        u'-'            # Miscellaneous Technical
        u'-'            # General Punctuation
        u'-'            # Superscripts and Subscripts / Currency / Letterlike
        u'-'            # Arrows
        u'-'            # Dingbats
        u']+', flags=re.UNICODE
    )
    return emoji_pattern.sub('', text)

def clean_project():
    root_dir = '.'
    # Files to ignore
    ignore_dirs = {'.venv', '.git', '__pycache__'}

    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]

        for file in files:
            if file.endswith(('.py', '.md', '.ms', '.txt')):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    cleaned_content = remove_emojis(content)

                    if cleaned_content != content:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(cleaned_content)
                        print(f"Cleaned: {file_path}")
                except Exception as e:
                    print(f"Error cleaning {file_path}: {e}")

if __name__ == "__main__":
    clean_project()
