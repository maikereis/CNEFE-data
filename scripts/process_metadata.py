import sys
from pathlib import Path

import pandas as pd

HEADER_POS = 6

MUNICIPALITY_FILE = "RELATORIO_DTB_BRASIL_2024_MUNICIPIOS.xls"
MUNICIPALITY_COLUMNS = [
    "UF",
    "Nome_UF",
    "Código Município Completo",
    "Nome_Município",
]

DISTRITAL_FILE = "RELATORIO_DTB_BRASIL_2024_DISTRITOS.xls"
DISTRITAL_COLUMNS = [
    "Código Município Completo",
    "Código de Distrito Completo",
    "Nome_Distrito",
]

SUBDISTRITAL_FILE = "RELATORIO_DTB_BRASIL_2024_SUBDISTRITOS.xls"
SUBDISTRITAL_COLUMNS = [
    "Código de Distrito Completo",
    "Código de Subdistrito Completo",
    "Nome_Subdistrito",
]

MUNICIPALITY_ID = "Código Município Completo"
DISTRITAL_ID = "Código de Distrito Completo"


def main(source: Path, output_filepath: Path):

    mun_filepath = Path(source, MUNICIPALITY_FILE)
    df_mun = pd.read_excel(
        mun_filepath,
        skiprows=HEADER_POS,
        usecols=MUNICIPALITY_COLUMNS,
    )

    dis_filepath = Path(source, DISTRITAL_FILE)
    df_dis = pd.read_excel(
        dis_filepath,
        skiprows=HEADER_POS,
        usecols=DISTRITAL_COLUMNS,
    )

    sub_filepath = Path(source, SUBDISTRITAL_FILE)
    df_sub = pd.read_excel(
        sub_filepath,
        skiprows=HEADER_POS,
        usecols=SUBDISTRITAL_COLUMNS,
    )

    df_merged = df_mun.merge(df_dis, on=MUNICIPALITY_ID).merge(
        df_sub, on=DISTRITAL_ID
    )

    Path(output_filepath).parent.mkdir(exist_ok=True, parents=True)

    df_merged.to_csv(output_filepath, index=0)


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]))
