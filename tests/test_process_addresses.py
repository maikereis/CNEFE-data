import pytest
import sys
from pathlib import Path
import pandas as pd
import json
from unittest.mock import patch

sys.path.append(str(Path(__file__).resolve().parents[1]))
import scripts.process_addresses as process_addresses


@pytest.fixture
def tmp_source(tmp_path):
    source = tmp_path / "source"
    source.mkdir()

    csv_file = source / "addresses.csv"
    df = pd.DataFrame(
        {
            "COD_UNICO_ENDERECO": ["1", "2"],
            "COD_UF": ["11", "12"],
            "COD_MUNICIPIO": ["001", "002"],
            "COD_DISTRITO": ["01", "02"],
            "COD_SUBDISTRITO": ["001", "002"],
            "NUM_ENDERECO": ["100", None],
            "NOM_COMP_ELEM1": ["A", "B"],
            "VAL_COMP_ELEM1": ["X", None],
            "LATITUDE": [10.0, 20.0],
            "DSC_MODIFICADOR": ["SN", ""],
            "DSC_LOCALIDADE": ["bairro1", "bairro2"],
            "CEP": ["00001-000", "00002-000"],
            "NOM_TIPO_SEGLOGR": ["RUA", "AV"],
            "LONGITUDE": [30.0, 40.0],
            "NOM_SEGLOGR": ["rua1", "rua2"],
        }
    )
    df.to_csv(csv_file, sep=";", index=False)
    return source


@pytest.fixture
def tmp_metadata(tmp_path):
    metadata = tmp_path / "metadata"
    metadata.mkdir()

    mappings = {
        "state": {"11": "Estado1", "12": "Estado2"},
        "municipality": {"001": "Mun1", "002": "Mun2"},
        "distrital": {"01": "Dist1", "02": "Dist2"},
        "subdistrital": {"001": "Sub1", "002": "Sub2"},
    }

    for name, mapping in mappings.items():
        path = metadata / f"{name}_mapping.json"
        path.write_text(json.dumps(mapping), encoding="utf-8")

    return metadata


@pytest.fixture
def tmp_destination(tmp_path):
    return tmp_path / "destination"


def test_main_characterization(tmp_source, tmp_metadata, tmp_destination):
    # Act
    process_addresses.main(tmp_source, tmp_metadata, tmp_destination)

    # Assert
    output_files = list(tmp_destination.glob("*.csv"))
    assert len(output_files) == 1

    df_out = pd.read_csv(output_files[0])

    for col in [
        "ID_ENDERECO",
        "ESTADO",
        "MUNICIPIO",
        "BAIRRO",
        "NUMERO",
        "COMPLEMENTO",
    ]:
        assert col in df_out.columns

    assert df_out.loc[0, "NUMERO"] == "SN"
    assert df_out.loc[0, "COMPLEMENTO"] == "A X"
    assert df_out.loc[1, "COMPLEMENTO"] == "B"
