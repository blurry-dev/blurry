import asyncio
import concurrent.futures
from pathlib import Path
from typing import Optional

from wand.image import Image

from blurry.settings import get_build_directory
from blurry.settings import get_content_directory
from blurry.settings import SETTINGS

CONTENT_DIR = get_content_directory()

AVIF_COMPRESSION_QUALITY = SETTINGS["AVIF_COMPRESSION_QUALITY"]
IMAGE_WIDTHS = SETTINGS["IMAGE_WIDTHS"]
MAXIMUM_IMAGE_WIDTH = int(SETTINGS["MAXIMUM_IMAGE_WIDTH"])
THUMBNAIL_WIDTH = int(SETTINGS["THUMBNAIL_WIDTH"])

TARGET_IMAGE_WIDTHS = [w for w in IMAGE_WIDTHS if w < MAXIMUM_IMAGE_WIDTH]
TARGET_IMAGE_WIDTHS.append(MAXIMUM_IMAGE_WIDTH)
if THUMBNAIL_WIDTH not in TARGET_IMAGE_WIDTHS:
    TARGET_IMAGE_WIDTHS.append(THUMBNAIL_WIDTH)

TARGET_IMAGE_WIDTHS.sort()


def add_image_width_to_path(image_path: Path, width: int) -> Path:
    new_filename = str(image_path).replace(
        image_path.suffix, f"-{width}{image_path.suffix}"
    )
    return Path(new_filename)


async def convert_image_to_avif(image_path: Path, target_path: Optional[Path] = None):
    image_suffix = image_path.suffix
    if image_suffix in [".webp", ".gif"]:
        return
    avif_filepath = str(target_path or image_path).replace(image_suffix, ".avif")
    if Path(avif_filepath).exists():
        return
    with Image(filename=str(image_path)) as image:
        image.format = "avif"
        image.compression_quality = AVIF_COMPRESSION_QUALITY
        image.save(filename=avif_filepath)


async def generate_images_for_srcset(image_path: Path):
    BUILD_DIR = get_build_directory()
    if image_path.suffix in [".webp", ".gif"]:
        return
    with Image(filename=str(image_path)) as img:
        width = img.width
        # Convert original image
        build_path = BUILD_DIR / image_path.resolve().relative_to(CONTENT_DIR)
        await convert_image_to_avif(image_path=image_path, target_path=build_path)

        avif_files_to_create: list[Path] = []
        for target_width in get_widths_for_image_width(width):
            new_filepath = add_image_width_to_path(image_path, target_width)
            relative_filepath = new_filepath.resolve().relative_to(CONTENT_DIR)
            build_filepath = BUILD_DIR / relative_filepath
            if build_filepath.exists():
                continue
            with img.clone() as resized:
                resized.transform(resize=str(target_width))
                resized.save(filename=build_filepath)
                avif_files_to_create.append(build_filepath)

        with concurrent.futures.ProcessPoolExecutor() as executor:
            executor.map(
                lambda avif_file: asyncio.run(convert_image_to_avif(avif_file)),
                avif_files_to_create,
            )


def get_widths_for_image_width(image_width: int) -> list[int]:
    widths = [tw for tw in TARGET_IMAGE_WIDTHS if tw < image_width]
    if image_width < TARGET_IMAGE_WIDTHS[-1]:
        widths.append(image_width)
    return widths


def generate_srcset_string(image_path: str, image_widths: list[int]) -> str:
    srcset_entries = [
        f"{add_image_width_to_path(Path(image_path), w)} {w}w" for w in image_widths
    ]
    return ", ".join(srcset_entries)


def generate_sizes_string(image_widths: list[int]) -> str:
    if not image_widths:
        return ""
    # Ensure widths are in ascending order
    image_widths.sort()
    size_strings = []

    for width in image_widths[0:-1]:
        size_strings.append(f"(max-width: {width}px) {width}px")
    largest_width = image_widths[-1]
    size_strings.append(f"{largest_width}px")
    return ", ".join(size_strings)
