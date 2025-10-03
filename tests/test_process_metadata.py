import pytest
import sys
from pathlib import Path
import json
import pandas as pd
from unittest.mock import patch

sys.path.append(str(Path(__file__).resolve().parents[1]))
import scripts.process_metadata as process_metadata


@pytest.fixture
def tmp_output(tmp_path):
    return tmp_path / "output"


def test_main_characterization_patched(tmp_output):
    # Create minimal fake DataFrames
    df_sta_and_mun = pd.DataFrame(
        {
            "UF": ["11", "12"],
            "Nome_UF": ["Estado1", "Estado2"],
            "Código Município Completo": ["11001", "12001"],
            "Nome_Município": ["Mun1", "Mun2"],
        }
    )

    df_distrital = pd.DataFrame(
        {
            "Código de Distrito Completo": ["11001", "12001"],
            "Nome_Distrito": ["Dist1", "Dist2"],
        }
    )

    df_subdistrital = pd.DataFrame(
        {
            "Código de Subdistrito Completo": ["11001", "12001"],
            "Nome_Subdistrito": ["Sub1", "Sub2"],
        }
    )

    # Patch pd.read_excel to return these DataFrames instead of reading files
    with patch("pandas.read_excel") as mock_read:
        # The side_effect returns a DataFrame depending on the file argument
        def side_effect(filepath, *args, **kwargs):
            fname = Path(filepath).name
            if fname == process_metadata.STATE_MUNICIPALITY_FILE:
                return df_sta_and_mun
            elif fname == process_metadata.DISTRITAL_FILE:
                return df_distrital
            elif fname == process_metadata.SUBDISTRITAL_FILE:
                return df_subdistrital
            else:
                return pd.DataFrame()

        mock_read.side_effect = side_effect

        # Act
        process_metadata.main("fake_source", tmp_output)

    # Assert that all mapping files are created
    expected_files = [
        process_metadata.STATE_MAPPING_FILENAME,
        process_metadata.MUNICIPALITY_MAPPING_FILENAME,
        process_metadata.DISTRITAL_MAPPING_FILENAME,
        process_metadata.SUBDISTRITAL_MAPPING_FILENAME,
    ]
    for fname in expected_files:
        fpath = tmp_output / fname
        assert fpath.exists()
        data = json.loads(fpath.read_text(encoding="utf-8"))
        assert isinstance(data, dict)
        assert len(data) > 0

    # Spot check: first state mapping
    state_map = json.loads(
        (tmp_output / process_metadata.STATE_MAPPING_FILENAME).read_text(
            encoding="utf-8"
        )
    )
    assert state_map["11"] == "Estado1"
