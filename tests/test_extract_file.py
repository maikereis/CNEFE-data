import sys
import zipfile
from pathlib import Path

import pytest

sys.path.append(str(Path(__file__).resolve().parents[1]))
import scripts.extract as extractor


@pytest.fixture
def tmp_source(tmp_path):
    """Create a temporary source directory with a real ZIP file."""
    source = tmp_path / "source"
    source.mkdir()
    zip_file = source / "archive.zip"
    with zipfile.ZipFile(zip_file, "w") as zipf:
        zipf.writestr("file1.txt", "Hello World")
        zipf.writestr("file2.csv", "Data")
    return source


@pytest.fixture
def tmp_destination(tmp_path):
    """Create a temporary destination directory."""
    return tmp_path / "destination"


def test_main_extraction_real_zip(tmp_source, tmp_destination):
    # Arrange
    source_dir = tmp_source
    dest_dir = tmp_destination
    zip_files = list(source_dir.rglob("*.zip"))
    assert len(zip_files) == 1

    # Act
    extractor.main(source_dir, dest_dir, ".txt")

    # Assert
    extracted_files = list(dest_dir.rglob("*.txt"))
    assert len(extracted_files) == 1
    assert extracted_files[0].name == "file1.txt"

    non_txt_files = list(dest_dir.rglob("*.csv"))
    assert len(non_txt_files) == 0
