import sys
from ftplib import FTP
from pathlib import Path

from tqdm import tqdm

FTP_HOST = "ftp.ibge.gov.br"
FTP_DIR = "/Cadastro_Nacional_de_Enderecos_para_Fins_Estatisticos/Censo_Demografico_2022/Arquivos_CNEFE/CSV"
DICTIONARY_PATH = "Dicionario_CNEFE_Censo_2022.xls"
ADDRESSES_PATH = "UF"
CHUNK_SIZE = 1024 * 1024 * 100  # 100 MB


def download_file(ftp: FTP, remote_path: str, local_path: Path):
    """Download a file with tqdm progress bar."""
    total_size = ftp.size(remote_path)
    with (
        open(local_path, "wb") as f,
        tqdm(
            total=total_size,
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
            desc=local_path.name,
            leave=False,
        ) as pbar,
    ):

        def callback(data):
            f.write(data)
            pbar.update(len(data))

        ftp.retrbinary(f"RETR {remote_path}", callback, blocksize=CHUNK_SIZE)


def main(destination: Path):
    ftp = FTP(FTP_HOST, timeout=60)
    ftp.login()
    ftp.cwd(FTP_DIR)

    Path(destination).mkdir(exist_ok=True, parents=True)

    # Already downloaded files
    downloaded = [f.name for f in Path(destination).rglob("*")]

    # Collect all files to download (dictionary + ZIPs)
    files_to_download = [DICTIONARY_PATH]
    addresses_zip_files = ftp.nlst(ADDRESSES_PATH)
    files_to_download.extend(addresses_zip_files)

    # Filter out already downloaded
    files_to_download = [
        f for f in files_to_download if Path(destination, f).name not in downloaded
    ]

    print(f"Downloading {len(files_to_download)} files...")

    # Overall progress bar
    with tqdm(total=len(files_to_download), desc="Total", unit="file") as overall_pbar:
        for filename in files_to_download:
            local_path = Path(destination, filename)
            local_path.parent.mkdir(exist_ok=True, parents=True)
            download_file(ftp, filename, local_path)
            overall_pbar.update(1)

    ftp.quit()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python download_cnefe.py <destination>")
    main(Path(sys.argv[1]))
