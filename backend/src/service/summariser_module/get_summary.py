import os
import base64
from pathlib import Path


def get_markdown(folder_id, folder_name):

    base_dir = os.getcwd()
    folder_path = base_dir + f"/resources/{folder_id}/{folder_name}/output/{folder_name}_parsed.md"
    text = Path(folder_path).resolve().read_text(encoding="utf-8")

    return {"page_1": text, "page_2": text}


def get_document_data(folder_id, folder_name):

    base_dir = os.getcwd()
    image_path = base_dir + f"/resources/{folder_id}/{folder_name}/output/{folder_name}_annotated.png"

    image_path = Path(image_path)
    with open(image_path, "rb") as f:
        img_bytes = f.read()

    img_b64 = base64.b64encode(img_bytes).decode("utf-8")

    metadata = get_markdown(folder_id, folder_name)

    return {"page_1": img_b64, "page_2": metadata["page_2"]}

