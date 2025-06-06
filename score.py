import os
import platform

def get_save_folder(app_name="GeometryWhores"):
    system = platform.system()

    if system == "Windows":
        appdata = os.getenv("APPDATA")
        if not appdata:
            appdata = os.path.expanduser("~\\AppData\\Roaming")
        folder = os.path.join(appdata, app_name)

    elif system == "Darwin":
        folder = os.path.join(os.path.expanduser("~/Library/Application Support"), app_name)

    else: 
        folder = os.path.join(os.path.expanduser("~/.config"), app_name)

    os.makedirs(folder, exist_ok=True)
    return folder

def get_high_score_file():
    return os.path.join(get_save_folder(), "highscore.txt")

def load_high_score():
    try:
        with open(get_high_score_file(), "r") as file:
            return int(file.read())
    except (FileNotFoundError, ValueError):
        return 0

def save_high_score(score):
    with open(get_high_score_file(), "w") as file:
        file.write(str(score))

def reset_score():
    return 0
