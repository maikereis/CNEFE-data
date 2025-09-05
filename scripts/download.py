import sys
from ftplib import FTP
from pathlib import Path

FTP_HOST = "ftp.ibge.gov.br"
FTP_DIR = "/Cadastro_Nacional_de_Enderecos_para_Fins_Estatisticos/Censo_Demografico_2022/Arquivos_CNEFE/CSV"
DICTIONARY_PATH = "Dicionario_CNEFE_Censo_2022.xls"
ADDRESSES_PATH = "UF"

def main(destination: Path):
    ftp = FTP(FTP_HOST, timeout=30)
    ftp.login()

    ftp.cwd(FTP_DIR)
    Path(destination).mkdir(exist_ok=True, parents=True)

    # Get already downloaded file names
    downloaded = [f.name for f in Path(destination).rglob('*')]

    if DICTIONARY_PATH not in downloaded:
        with open(Path(destination, DICTIONARY_PATH), "wb") as f:
            ftp.retrbinary(f"RETR {DICTIONARY_PATH}", f.write)

    # Get list of ZIP files inside "UF" directory
    addresses_zip_files = ftp.nlst(ADDRESSES_PATH)

    Path(destination, ADDRESSES_PATH).mkdir(exist_ok=True, parents=True)

    for filename in addresses_zip_files:
        local_path = Path(destination, filename)
        if local_path.name not in downloaded:
            print(f"Downloading {filename}...")
            with open(local_path, "wb") as f:
                ftp.retrbinary(f"RETR {filename}", f.write)

    ftp.quit()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)
    main(Path(sys.argv[1]))
