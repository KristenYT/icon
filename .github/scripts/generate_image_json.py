import json
import os

IMAGE_FOLDERS = ["Badges", "Emby", "Other", "Rex", "Surge", "VideoPlayer"]
IMAGE_EXTENSIONS = {".png", ".webp"}


def generate_json():
    repo = os.environ["GITHUB_REPOSITORY"]
    icons = []
    seen = set()
    for folder in IMAGE_FOLDERS:
        if not os.path.isdir(folder):
            continue
        for root, dirs, files in os.walk(folder):
            dirs.sort()
            for filename in sorted(files):
                _, ext = os.path.splitext(filename)
                if ext.lower() not in IMAGE_EXTENSIONS:
                    continue
                rel_dir = os.path.relpath(root, folder)
                rel_path = filename if rel_dir == "." else f"{rel_dir}/{filename}"
                url_path = f"{folder}/{rel_path}".replace(os.sep, "/")
                name = os.path.splitext(filename)[0]
                prefix_parts = []
                if rel_dir != ".":
                    prefix_parts = [rel_dir.replace(os.sep, "_")]
                while name in seen:
                    if prefix_parts:
                        name = f"{prefix_parts.pop(0)}_{name}"
                    else:
                        name = f"{folder}_{name}"
                seen.add(name)
                url = f"https://raw.githubusercontent.com/{repo}/main/{url_path}"
                icons.append({"name": name, "url": url})
    try:
        with open("icon.json", "r", encoding="utf-8") as old_file:
            old_data = json.load(old_file)
        prefix = f"https://raw.githubusercontent.com/{repo}/main/"
        for icon in old_data.get("icons", []):
            url = icon.get("url", "")
            if url and not url.startswith(prefix):
                if icon.get("name") not in seen:
                    seen.add(icon["name"])
                    icons.append(icon)
    except (FileNotFoundError, ValueError):
        pass
    json_data = {"name": "icons", "description": "", "icons": icons}
    with open("icon.json", "w", encoding="utf-8") as json_file:
        json.dump(json_data, json_file, ensure_ascii=False, indent=2)
    github_state = os.environ.get("GITHUB_STATE")
    if github_state:
        with open(github_state, "a", encoding="utf-8") as state_file:
            state_file.write("ICONS_JSON_PATH=icon.json\n")


if __name__ == "__main__":
    generate_json()
