import sys
import json
import pandas as pd
from pathlib import Path
from typing import Dict, Iterator
from tqdm import tqdm


CHUNKSIZE = 250_000

COLUMNS = [
    "COD_UNICO_ENDERECO", "COD_UF", "COD_MUNICIPIO", "COD_DISTRITO",
    "COD_SUBDISTRITO", "NUM_ENDERECO", "NOM_COMP_ELEM1", "VAL_COMP_ELEM1",
    "LATITUDE", "DSC_MODIFICADOR", "DSC_LOCALIDADE", "CEP",
    "NOM_TIPO_SEGLOGR", "LONGITUDE", "NOM_SEGLOGR"
]

DTYPES = {
    "COD_UF": "string",
    "COD_MUNICIPIO": "string",
    "COD_DISTRITO": "string",
    "COD_SUBDISTRITO": "string",
    "NUM_ENDERECO": "string",
    "LATITUDE": "float",
    "LONGITUDE": "float",
}


def load_mappings(metadata: Path) -> Dict[str, Dict[str, str]]:
    """Load all mapping JSON files from metadata directory."""
    mappings = {}
    for name in ["state", "municipality", "distrital", "subdistrital"]:
        path = metadata / f"{name}_mapping.json"
        with open(path, "r", encoding="utf-8") as f:
            mappings[name] = json.load(f)
    return mappings


def process_chunk(df: pd.DataFrame, mappings: Dict[str, Dict[str, str]]) -> pd.DataFrame:
    """Process a single dataframe chunk and return cleaned dataframe."""
    df["ESTADO"] = df["COD_UF"].map(mappings["state"])
    df["MUNICIPIO"] = df["COD_MUNICIPIO"].map(mappings["municipality"])
    df["DISTRITO"] = df["COD_DISTRITO"].map(mappings["distrital"])
    df["SUBDISTRITO"] = df["COD_SUBDISTRITO"].map(mappings["subdistrital"])

    # Clean complemento fields
    df["COMPLEMENTO"] = (
        df[["NOM_COMP_ELEM1", "VAL_COMP_ELEM1"]]
        .fillna("")
        .astype(str)
        .agg(" ".join, axis=1)
        .str.split()
        .str.join(" ")
    )

    # Replace by SN (sem número)
    df.loc[df["DSC_MODIFICADOR"] == "SN", "NUM_ENDERECO"] = "SN"

    # Filter only required columns
    df = df.filter(
        items=[
            "COD_UNICO_ENDERECO", "ESTADO", "MUNICIPIO", "DISTRITO",
            "SUBDISTRITO", "DSC_LOCALIDADE", "CEP", "NOM_TIPO_SEGLOGR", "NOM_SEGLOGR",
            "NUM_ENDERECO", "COMPLEMENTO", "LATITUDE", "LONGITUDE"
        ]
    )

    return df.rename(
        columns={
            "COD_UNICO_ENDERECO": "ID_ENDERECO",
            "DSC_LOCALIDADE": "BAIRRO",
            "NOM_SEGLOGR":"RUA",
            "NOM_TIPO_SEGLOGR": "TIPO_LOGRADOURO",
            "NUM_ENDERECO": "NUMERO"
        }
    )


def process_file(filepath: Path, destination: Path, mappings: Dict[str, Dict[str, str]]):
    """Process a single CSV file in chunks and save results."""
    output_file = destination / filepath.name
    first_chunk = True

    # Count lines for progress bar estimation
    total_lines = sum(1 for _ in open(filepath, "r", encoding="utf-8")) - 1  # skip header
    total_chunks = (total_lines // CHUNKSIZE) + 1

    chunk_iter: Iterator[pd.DataFrame] = pd.read_csv(
        filepath,
        sep=";",
        usecols=COLUMNS,
        dtype=DTYPES,
        chunksize=CHUNKSIZE,
        low_memory=False,
    )

    with tqdm(
        total=total_chunks,
        desc=f"Processing {filepath.name}",
        unit="chunk"
    ) as pbar:
        for chunk in chunk_iter:
            processed = process_chunk(chunk, mappings)
            processed.to_csv(
                output_file,
                index=False,
                mode="w" if first_chunk else "a",
                header=first_chunk,
            )
            first_chunk = False
            pbar.update(1)


def main(source: Path, metadata: Path, destination: Path):
    """Main pipeline for processing multiple CSV files."""
    destination.mkdir(exist_ok=True, parents=True)

    mappings = load_mappings(metadata)
    files = sorted(Path(source).rglob("*.csv"))

    with tqdm(total=len(files), desc="Overall Progress", unit="file") as pbar:
        for filepath in files:
            process_file(filepath, destination, mappings)
            pbar.update(1)


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python script.py <source> <metadata> <destination>")
        sys.exit(1)

    main(Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]))
