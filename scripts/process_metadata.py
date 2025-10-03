import json
import sys
from pathlib import Path

import pandas as pd

HEADER_POS = 6

STATE_MUNICIPALITY_FILE = "RELATORIO_DTB_BRASIL_2024_MUNICIPIOS.xls"
STATE_COLUMNS = [
    "UF",
    "Nome_UF",
]

STATE_MAPPING_FILENAME = "state_mapping.json"

MUNICIPALITY_COLUMNS = [
    "Código Município Completo",
    "Nome_Município",
]
MUNICIPALITY_MAPPING_FILENAME = "municipality_mapping.json"


DISTRITAL_FILE = "RELATORIO_DTB_BRASIL_2024_DISTRITOS.xls"
DISTRITAL_COLUMNS = [
    "Código de Distrito Completo",
    "Nome_Distrito",
]
DISTRITAL_MAPPING_FILENAME = "distrital_mapping.json"


SUBDISTRITAL_FILE = "RELATORIO_DTB_BRASIL_2024_SUBDISTRITOS.xls"
SUBDISTRITAL_COLUMNS = [
    "Código de Subdistrito Completo",
    "Nome_Subdistrito",
]
SUBDISTRITAL_MAPPING_FILENAME = "subdistrital_mapping.json"


def main(source: Path, output_dir: Path):

    Path(output_dir).mkdir(parents=True, exist_ok=True)

    mun_filepath = Path(source, STATE_MUNICIPALITY_FILE)
    df_sta_and_mun = pd.read_excel(
        mun_filepath,
        skiprows=HEADER_POS,
        usecols=STATE_COLUMNS + MUNICIPALITY_COLUMNS,
    )

    df_state = df_sta_and_mun[STATE_COLUMNS]

    state_mapping = dict(df_state.drop_duplicates().values)

    with open(output_dir / STATE_MAPPING_FILENAME, "w", encoding="utf-8") as file:
        print(f"Creating states mapping file...")
        json.dump(state_mapping, file, ensure_ascii=False)

    df_municipality = df_sta_and_mun[MUNICIPALITY_COLUMNS]
    municipality_mapping = dict(df_municipality.drop_duplicates().values)

    with open(
        output_dir / MUNICIPALITY_MAPPING_FILENAME, "w", encoding="utf-8"
    ) as file:
        print(f"Creating municipality mapping file...")
        json.dump(municipality_mapping, file, ensure_ascii=False)

    dis_filepath = Path(source, DISTRITAL_FILE)
    df_distrital = pd.read_excel(
        dis_filepath,
        skiprows=HEADER_POS,
        usecols=DISTRITAL_COLUMNS,
    )
    distrital_mapping = dict(df_distrital.drop_duplicates().values)

    with open(output_dir / DISTRITAL_MAPPING_FILENAME, "w", encoding="utf-8") as file:
        print(f"Creating distrital mapping file...")
        json.dump(distrital_mapping, file, ensure_ascii=False)

    sub_filepath = Path(source, SUBDISTRITAL_FILE)
    df_subdistrital = pd.read_excel(
        sub_filepath,
        skiprows=HEADER_POS,
        usecols=SUBDISTRITAL_COLUMNS,
    )
    subdistrital_mapping = dict(df_subdistrital.drop_duplicates().values)
    with open(
        output_dir / SUBDISTRITAL_MAPPING_FILENAME, "w", encoding="utf-8"
    ) as file:
        print(f"Creating subdistrital mapping file...")
        json.dump(subdistrital_mapping, file, ensure_ascii=False)


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]))
