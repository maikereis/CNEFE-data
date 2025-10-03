import sys
from pathlib import Path
from unittest.mock import Mock, patch

sys.path.append(str(Path(__file__).resolve().parents[1]))

import scripts.download as download_cnefe


def test_download_file_characterization(tmp_path):
    # Arrange
    fake_ftp = Mock()
    fake_ftp.size.return_value = 10
    chunks = [b"012345", b"abcdef"]

    def fake_retrbinary(cmd, callback, blocksize):
        for c in chunks:
            callback(c)

    fake_ftp.retrbinary.side_effect = fake_retrbinary

    local_path = tmp_path / "test_file.txt"

    # Act
    download_cnefe.download_file(fake_ftp, "remote/file.txt", local_path)

    # Assert
    assert local_path.read_bytes() == b"012345abcdef"
    fake_ftp.size.assert_called_once_with("remote/file.txt")
    fake_ftp.retrbinary.assert_called_once()


@patch("scripts.download.FTP")
def test_main_characterization(mock_ftp_class, tmp_path):
    # Arrange
    fake_ftp = Mock()
    fake_ftp.nlst.return_value = ["UF/file1.zip", "UF/file2.zip"]
    fake_ftp.size.return_value = 10
    mock_ftp_class.return_value = fake_ftp

    # Act
    download_cnefe.main(tmp_path)

    # Assert: we expect 3 downloads (dictionary + 2 zips)
    calls = [call[0][0] for call in fake_ftp.retrbinary.call_args_list]
    assert any("Dicionario_CNEFE_Censo_2022.xls" in c for c in calls)
    assert any("UF/file1.zip" in c for c in calls)
    assert any("UF/file2.zip" in c for c in calls)
