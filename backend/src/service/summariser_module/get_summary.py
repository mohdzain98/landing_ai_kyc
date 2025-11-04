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
    output_path = Path(base_dir + f"/resources/{folder_id}/{folder_name}/output/")

    matched_files = [f for f in output_path.iterdir() if
                     f.is_file() and f.name.endswith((".png", ".PNG")) and "page_" in f.name]

    matched_files.sort(key=lambda f: int(f.stem.split("_")[-1]))

    images = list()

    for image_path in matched_files:

        image_path = Path(image_path)
        with open(image_path, "rb") as f:
            img_bytes = f.read()

        img_b64 = base64.b64encode(img_bytes).decode("utf-8")

        images.append(img_b64)

    metadata = get_markdown(folder_id, folder_name)

    return {"images": images, "kpis": metadata["page_2"]}

