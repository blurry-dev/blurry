import concurrent.futures
from pathlib import Path

from wand.image import Image

from blurry.settings import get_build_directory
from blurry.settings import get_content_directory
from blurry.settings import SETTINGS
from blurry.settings import update_settings


def get_target_image_widths():
    update_settings()
    IMAGE_WIDTHS = SETTINGS["IMAGE_WIDTHS"]
    MAXIMUM_IMAGE_WIDTH = int(SETTINGS["MAXIMUM_IMAGE_WIDTH"])
    THUMBNAIL_WIDTH = int(SETTINGS["THUMBNAIL_WIDTH"])

    TARGET_IMAGE_WIDTHS = [w for w in IMAGE_WIDTHS if w < MAXIMUM_IMAGE_WIDTH]
    TARGET_IMAGE_WIDTHS.append(MAXIMUM_IMAGE_WIDTH)
    if THUMBNAIL_WIDTH not in TARGET_IMAGE_WIDTHS:
        TARGET_IMAGE_WIDTHS.append(THUMBNAIL_WIDTH)

    return sorted(TARGET_IMAGE_WIDTHS)


def add_image_width_to_path(image_path: Path, width: int) -> Path:
    new_filename = str(image_path).replace(
        image_path.suffix, f"-{width}{image_path.suffix}"
    )
    return Path(new_filename)


def convert_image_to_avif(image_path: Path, target_path: Path | None = None):
    AVIF_COMPRESSION_QUALITY = SETTINGS["AVIF_COMPRESSION_QUALITY"]
    image_suffix = image_path.suffix
    avif_filepath = str(target_path or image_path).replace(image_suffix, ".avif")
    if Path(avif_filepath).exists():
        return
    with Image(filename=str(image_path)) as image:
        image.format = "avif"
        image.compression_quality = AVIF_COMPRESSION_QUALITY
        image.save(filename=avif_filepath)


def clone_and_resize_image(
    image: Image, target_width: int, resized_image_destination: Path
):
    if resized_image_destination.exists():
        return
    image.transform(resize=str(target_width))
    image.save(filename=resized_image_destination)


async def generate_images_for_srcset(image_path: Path):
    BUILD_DIR = get_build_directory()
    CONTENT_DIR = get_content_directory()
    filepaths_to_convert_to_avif = []

    build_path = BUILD_DIR / image_path.resolve().relative_to(CONTENT_DIR)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        with Image(filename=str(image_path)) as img:
            width = img.width

            for target_width in get_widths_for_image_width(width):
                new_filepath = add_image_width_to_path(image_path, target_width)
                relative_filepath = new_filepath.resolve().relative_to(CONTENT_DIR)
                build_filepath = BUILD_DIR / relative_filepath
                # We convert the resized images to AVIF, so do this synchronously
                clone_and_resize_image(img, target_width, build_filepath)
                filepaths_to_convert_to_avif.append(build_filepath)

        # Convert original image
        executor.submit(
            convert_image_to_avif, image_path=image_path, target_path=build_path
        )
        # Generate AVIF files for resized images
        executor.map(convert_image_to_avif, filepaths_to_convert_to_avif)


def get_widths_for_image_width(image_width: int) -> list[int]:
    target_image_widths = get_target_image_widths()
    widths = [tw for tw in target_image_widths if tw < image_width]
    if image_width < target_image_widths[-1]:
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
