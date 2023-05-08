from pathlib import Path

import ffmpeg
from mistune.util import escape


def render_video(src: str, absolute_path: Path, extension: str, title: str | None):
    video_probe_output = ffmpeg.probe(absolute_path)
    video_info = video_probe_output["streams"][0]
    video_width = video_info["width"]
    video_height = video_info["height"]

    video_attributes = {
        "height": video_height,
        "width": video_width,
    }
    if title:
        video_attributes["title"] = escape(title)

    video_attributes_str = " ".join(
        f'{name}="{value}"' for name, value in video_attributes.items()
    )

    mimetype = f"video/{extension}"
    return (
        f"<video {video_attributes_str} controls>"
        f'<source src="{src}" type="{mimetype}"></source></video>'
    )
