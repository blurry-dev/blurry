import pytest

from blurry.images import generate_sizes_string
from blurry.images import generate_srcset_string
from blurry.images import get_widths_for_image_width


@pytest.mark.parametrize(
    "image_path, image_widths, expected_output",
    [
        (
            "dummy_image.png",
            [100, 200, 800],
            (
                "dummy_image-100.png 100w, dummy_image-200.png 200w, "
                "dummy_image-800.png 800w"
            ),
        ),
        (
            "dummy_image.avif",
            [240, 800],
            "dummy_image-240.avif 240w, dummy_image-800.avif 800w",
        ),
        (
            "dummy_image.webp",
            [240, 800],
            "dummy_image-240.webp 240w, dummy_image-800.webp 800w",
        ),
    ],
)
def test_generate_srcset_string(
    image_path: str, image_widths: list[int], expected_output: str
):
    srcset_string = generate_srcset_string(image_path, image_widths)
    assert srcset_string == expected_output


@pytest.mark.parametrize(
    "image_widths, expected_output",
    [
        (
            [100, 200, 800],
            "(max-width: 100px) 100px, (max-width: 200px) 200px, 800px",
        ),
        (
            [200, 400],
            "(max-width: 200px) 200px, 400px",
        ),
        ([240], "240px"),
    ],
)
def test_generate_sizes_string(image_widths: list[int], expected_output: str):
    sizes_string = generate_sizes_string(image_widths)
    assert sizes_string == expected_output


@pytest.mark.parametrize(
    "image_width, expected_output",
    [
        (900, [250, 360, 640, 768, 900]),
        (700, [250, 360, 640, 700]),
        (768, [250, 360, 640, 768]),
        (249, [249]),
    ],
)
def test_get_widths_for_image_width(image_width: int, expected_output: list[int]):
    image_widths = get_widths_for_image_width(image_width)
    assert image_widths == expected_output
