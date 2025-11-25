import concurrent.futures
from concurrent.futures import Future
from pathlib import Path

from PIL import Image

from blurry.settings import get_build_directory
from blurry.settings import get_content_directory
from blurry.settings import get_settings
from blurry.utils import handle_future_result


def get_target_image_widths():
    SETTINGS = get_settings()
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
    SETTINGS = get_settings()
    IMAGE_COMPRESSION_QUALITY = SETTINGS["IMAGE_COMPRESSION_QUALITY"]
    new_filepath = (target_path or image_path).with_suffix(".avif")
    if Path(new_filepath).exists():
        return
    with Image.open(image_path) as image:
        image.save(new_filepath, quality=IMAGE_COMPRESSION_QUALITY)


def clone_and_resize_image_as_avif_or_webp(image_path: Path, target_width: int):
    resized_image_suffix = ".webp" if image_path.suffix == ".webp" else ".avif"
    resized_image_destination = get_build_directory() / (
        add_image_width_to_path(
            image_path.with_suffix(resized_image_suffix), target_width
        )
    ).relative_to(get_content_directory())
    if resized_image_destination.exists():
        return
    with Image.open(image_path) as image:
        width, height = image.size
        resize_factor = target_width / width
        resized_image = image.resize(
            (target_width, int(height * resize_factor)), Image.Resampling.LANCZOS
        )
        resized_image.save(resized_image_destination)


async def generate_images_for_srcset(image_path: Path):
    BUILD_DIR = get_build_directory()
    CONTENT_DIR = get_content_directory()
    image_futures: list[Future] = []

    build_path = BUILD_DIR / image_path.resolve().relative_to(CONTENT_DIR)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Convert original image only if it is in an inefficient format
        if image_path.suffix not in [".avif", ".webp"]:
            full_sized_image_future = executor.submit(
                convert_image_to_avif, image_path=image_path, target_path=build_path
            )
            full_sized_image_future.add_done_callback(
                lambda future: handle_future_result(
                    future,
                    f"Could not convert image: {image_path.relative_to(CONTENT_DIR)}",
                )
            )
            image_futures.append(full_sized_image_future)

        width = Image.open(image_path).width

        for target_width in get_widths_for_image_width(width):
            resized_image_future = executor.submit(
                clone_and_resize_image_as_avif_or_webp, image_path, target_width
            )
            resized_image_future.add_done_callback(
                lambda future: handle_future_result(
                    future,
                    f"Could not resize image: {image_path.relative_to(CONTENT_DIR)} to {target_width}",
                )
            )
            image_futures.append(resized_image_future)

    concurrent.futures.wait(image_futures)


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
