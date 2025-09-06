import sys
from pathlib import Path
from zipfile import BadZipFile, ZipFile


def main(source: Path, destination: Path, extension=None):
    """
    Extract files from zip archives in `source` to `destination`.
    Only extracts files with specified `extensions`.
    """
    Path(destination).mkdir(exist_ok=True, parents=True)

    # List all zip files in source recursively
    files = [file for file in Path(source).rglob("*.zip")]

    # List already extracted files to avoid duplicates
    extracted = [file.name for file in Path(destination).rglob("*")]

    for file_path in files:
        try:
            with ZipFile(file_path, "r") as ref:
                content_list = ref.namelist()
                # Filter files by extension and skip already extracted
                extract_files = [
                    content
                    for content in content_list
                    if Path(content).suffix.lower() == extension
                    and Path(content).name not in extracted
                ]

                for file in extract_files:
                    ref.extract(file, destination)
        except BadZipFile:
            print(f"{file_path} file is corrupted.")
            continue


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]), str(sys.argv[3]))
