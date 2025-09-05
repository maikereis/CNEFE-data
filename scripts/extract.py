import sys
from zipfile import ZipFile, BadZipFile
from pathlib import Path

def main(source: Path, destination: Path):

    Path(destination).mkdir(exist_ok=True, parents=True)

    files = [file for file in Path(source).rglob("*") if '.zip' in file.name]

    extracted = [file.name for file in Path(destination).rglob("*")]

    for file_path in files:
        try: 
            with ZipFile(file_path, 'r') as ref:
                content_list = ref.namelist()
                extract_files = [content for content in content_list if content not in extracted]
                for file in extract_files:
                    ref.extract(file, destination)
        except BadZipFile:
            print(f"{file_path} file is corrupted.")
            continue

if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]))