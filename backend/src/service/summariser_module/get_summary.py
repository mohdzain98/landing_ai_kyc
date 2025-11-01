import os
from pathlib import Path


def get_markdown(folder_id, folder_name):

    base_dir = os.getcwd()
    folder_path = base_dir + f"/resources/{folder_id}/{folder_name}/output/{folder_name}_parsed.md"
    text = Path(folder_path).resolve().read_text(encoding="utf-8")

    return text
