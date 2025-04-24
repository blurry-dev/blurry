import concurrent.futures
from concurrent.futures import Future
from pathlib import Path

from wand.image import Image

from blurry.settings import get_build_directory
from blurry.settings import get_content_directory
from blurry.settings import get_settings


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
    image_path: Path, target_width: int, resized_image_destination: Path
):
    if resized_image_destination.exists():
        return
    with Image(filename=str(image_path)) as image:
        image.transform(resize=str(target_width))
        image.save(filename=resized_image_destination)


async def generate_images_for_srcset(image_path: Path):
    BUILD_DIR = get_build_directory()
    CONTENT_DIR = get_content_directory()
    image_futures: list[Future] = []

    build_path = BUILD_DIR / image_path.resolve().relative_to(CONTENT_DIR)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Convert original image
        full_sized_avif_future = executor.submit(
            convert_image_to_avif, image_path=image_path, target_path=build_path
        )
        image_futures.append(full_sized_avif_future)

        # Store resized image futures so AVIF versions can be created once they're done
        resize_future_to_filepath: dict[Future, Path] = {}

        width = Image(filename=str(image_path)).width

        for target_width in get_widths_for_image_width(width):
            new_filepath = add_image_width_to_path(image_path, target_width)
            new_filepath_in_build = BUILD_DIR / new_filepath.relative_to(CONTENT_DIR)

            resized_original_image_type_future = executor.submit(
                clone_and_resize_image, image_path, target_width, new_filepath_in_build
            )
            resize_future_to_filepath[resized_original_image_type_future] = (
                new_filepath_in_build
            )

        # Create AVIF versions of resized images as they're ready
        for future in concurrent.futures.as_completed(resize_future_to_filepath):
            resized_image_filepath = resize_future_to_filepath[future]
            resized_avif_future = executor.submit(
                convert_image_to_avif, resized_image_filepath
            )
            image_futures.append(resized_avif_future)

        concurrent.futures.wait(image_futures + list(resize_future_to_filepath.keys()))


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
