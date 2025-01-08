import concurrent.futures
from pathlib import Path

from blurry.markdown import convert_markdown_file_to_html
from blurry.settings import get_content_directory
from blurry.types import DirectoryFileData
from blurry.types import MarkdownFileData


def sort_directory_file_data_by_date(
    directory_file_data: DirectoryFileData,
) -> DirectoryFileData:
    for path, file_data in directory_file_data.items():
        file_data.sort(
            key=lambda page: str(page.front_matter.get("datePublished", ""))
            or str(page.front_matter.get("dateCreated", ""))
            or "0000-00-00",
            reverse=True,
        )
        directory_file_data[path] = file_data

    return directory_file_data


def gather_file_data_by_directory() -> DirectoryFileData:
    # Sort file data by publishedDate/createdDate, descending, if present
    file_data_by_directory: DirectoryFileData = {}
    content_directory = get_content_directory()

    markdown_future_to_path: dict[concurrent.futures.Future, Path] = {}
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for filepath in content_directory.rglob("*.md"):
            # Extract filepath for storing context data and writing out
            relative_filepath = filepath.relative_to(content_directory)

            # Convert Markdown file to HTML
            future = executor.submit(convert_markdown_file_to_html, filepath)
            markdown_future_to_path[future] = relative_filepath

        for future in concurrent.futures.as_completed(markdown_future_to_path):
            body, front_matter = future.result()
            relative_filepath = markdown_future_to_path[future]
            if exception := future.exception():
                print(
                    f"{relative_filepath}: Could not convert file to HTML - {exception}"
                )
            file_data = MarkdownFileData(
                body=body,
                front_matter=front_matter,
                path=relative_filepath,
            )
            parent_directory = relative_filepath.parent
            try:
                file_data_by_directory[parent_directory].append(file_data)
            except KeyError:
                file_data_by_directory[parent_directory] = [file_data]

    concurrent.futures.wait(markdown_future_to_path)

    return sort_directory_file_data_by_date(file_data_by_directory)
