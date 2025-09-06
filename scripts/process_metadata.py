import sys
from pathlib import Path

import pandas as pd


def main(source: Path, destination: Path):

    mun_filepath = Path(source, "RELATORIO_DTB_BRASIL_2024_MUNICIPIOS.xls")
    df_mun = pd.read_excel(
        mun_filepath,
        skiprows=6,
        usecols=["UF", "Nome_UF", "Código Município Completo", "Nome_Município"],
    )

    dis_filepath = Path(source, "RELATORIO_DTB_BRASIL_2024_DISTRITOS.xls")
    df_dis = pd.read_excel(
        dis_filepath,
        skiprows=6,
        usecols=[
            "Código Município Completo",
            "Código de Distrito Completo",
            "Nome_Distrito",
        ],
    )

    sub_filepath = Path(source, "RELATORIO_DTB_BRASIL_2024_SUBDISTRITOS.xls")
    df_sub = pd.read_excel(
        sub_filepath,
        skiprows=6,
        usecols=[
            "Código de Distrito Completo",
            "Código de Subdistrito Completo",
            "Nome_Subdistrito",
        ],
    )

    df_merged = df_mun.merge(df_dis, on=["Código Município Completo"]).merge(
        df_sub, on=["Código de Distrito Completo"]
    )

    Path(destination).mkdir(exist_ok=True, parents=True)

    merged_filepath = Path(destination, "names.csv")

    df_merged.to_csv(merged_filepath, index=0)


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]))
