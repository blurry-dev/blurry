import asyncio
from pathlib import Path
from typing import Coroutine
from typing import Optional

from wand.image import Image

from blurry.constants import BUILD_DIR
from blurry.constants import CONTENT_DIR
from blurry.constants import IMAGE_WIDTHS
from blurry.settings import SETTINGS

MAXIMUM_IMAGE_WIDTH = SETTINGS["maximum_image_width"]

TARGET_IMAGE_WIDTHS = [w for w in IMAGE_WIDTHS if w < MAXIMUM_IMAGE_WIDTH]
TARGET_IMAGE_WIDTHS.insert(0, MAXIMUM_IMAGE_WIDTH)


def add_image_width_to_path(image_path: Path, width: int) -> Path:
    new_filename = str(image_path).replace(
        image_path.suffix, f"-{width}{image_path.suffix}"
    )
    return Path(new_filename)


async def convert_image_to_avif(image_path: Path, target_path: Optional[Path] = None):
    image_suffix = image_path.suffix
    avif_filepath = str(target_path or image_path).replace(image_suffix, ".avif")
    if Path(avif_filepath).exists():
        return
    with Image(filename=str(image_path)) as image:
        image.format = "avif"
        image.save(filename=avif_filepath)


async def generate_images_for_srcset(image_path: Path):
    tasks: list[Coroutine] = []
    with Image(filename=str(image_path)) as img:
        width = img.width
        # Convert original image
        build_path = BUILD_DIR / image_path.resolve().relative_to(CONTENT_DIR)
        await convert_image_to_avif(image_path=image_path, target_path=build_path)

        for target_width in TARGET_IMAGE_WIDTHS:
            if target_width > width:
                continue
            with img.clone() as resized:
                resized.transform(resize=str(target_width))
                new_filepath = add_image_width_to_path(image_path, target_width)
                relative_filepath = new_filepath.resolve().relative_to(CONTENT_DIR)
                build_filepath = BUILD_DIR / relative_filepath
                if not build_filepath.exists():
                    resized.save(filename=build_filepath)
                tasks.append(convert_image_to_avif(build_filepath))
        await asyncio.gather(*tasks)


def get_widths_for_image_width(image_width: int) -> list[int]:
    widths = [w for w in TARGET_IMAGE_WIDTHS if w <= image_width]
    return widths


def generate_srcset_string(image_path: str, image_widths: list[int]) -> str:
    srcset_entries = [
        f"{add_image_width_to_path(Path(image_path), w)} {w}w" for w in image_widths
    ]
    return ", ".join(srcset_entries)


def generate_sizes_string(image_widths: list[int]) -> str:
    return ", ".join(f"(max-width: {w}px) {w}px" for w in reversed(image_widths))
