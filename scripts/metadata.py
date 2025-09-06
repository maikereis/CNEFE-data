import sys
from ftplib import FTP
from pathlib import Path

FTP_HOST = "geoftp.ibge.gov.br"
FTP_DIR = "/organizacao_do_territorio/estrutura_territorial/divisao_territorial/2024/"
DTB_PATH = "DTB_2024.zip"


def main(destination: Path):
    ftp = FTP(FTP_HOST, timeout=30)
    ftp.login()

    ftp.cwd(FTP_DIR)
    Path(destination).mkdir(exist_ok=True, parents=True)

    with open(Path(destination, DTB_PATH), "wb") as f:
        ftp.retrbinary(f"RETR {DTB_PATH}", f.write)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)
    main(Path(sys.argv[1]))
