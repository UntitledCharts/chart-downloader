import io

import pjsk_background_gen_PIL as pjsk_bg
from PIL import Image
from pathlib import Path


def generate_backgrounds(path: Path):
    jacket_pil_image = Image.open(path)
    jacket_pil_image = jacket_pil_image.resize((1000, 1000)).convert("RGBA")
    v1 = pjsk_bg.render_v1(jacket_pil_image)
    v3 = pjsk_bg.render_v3(jacket_pil_image)
    folder_path = path.parent
    v1.save(folder_path / "background_v1.png", format="PNG")
    v3.save(folder_path / "background_v3.png", format="PNG")
