from pathlib import Path

from pymediainfo import MediaInfo
from mistune.util import escape


def render_video(src: str, absolute_path: Path, extension: str, title: str | None):
    media_info = MediaInfo.parse(absolute_path)
    video_width = 0
    video_height = 0
    for track in media_info.tracks:
        if track.track_type == "Video":
            video_width = track.width
            video_height = track.height

    if 0 in {video_width, video_height}:
        raise Exception("Video width and/or height undefined")

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
