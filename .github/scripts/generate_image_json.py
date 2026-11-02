import json
import os

IMAGE_FOLDERS = ["Badges", "Emby", "Rex", "Surge", "VideoPlayer"]
IMAGE_EXTENSIONS = {".png", ".webp"}


def generate_json():
    repo = os.environ["GITHUB_REPOSITORY"]
    icons = []
    seen = set()
    for folder in IMAGE_FOLDERS:
        if not os.path.isdir(folder):
            continue
        for filename in sorted(os.listdir(folder)):
            _, ext = os.path.splitext(filename)
            if ext.lower() not in IMAGE_EXTENSIONS:
                continue
            name = os.path.splitext(filename)[0]
            while name in seen:
                name = f"{folder}_{name}"
            seen.add(name)
            url = f"https://raw.githubusercontent.com/{repo}/main/{folder}/{filename}"
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
