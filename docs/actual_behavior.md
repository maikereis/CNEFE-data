# CNEFE Pipeline API Documentation

This document describes the actual behavior of each module in the CNEFE data pipeline, as verified by characterization tests.

---

## `scripts/download.py`

### `download_file()`

```python
def download_file(ftp: FTP, remote_path: str, local_path: Path) -> None
```

Downloads a file from an FTP server with progress tracking.

#### Parameters
- `ftp` (FTP): Active FTP connection object
- `remote_path` (str): Path to the file on the remote FTP server
- `local_path` (Path): Local filesystem path where file will be saved

#### Behavior
- Queries remote file size using `ftp.size(remote_path)`
- Downloads file using `ftp.retrbinary()` command
- Writes data in chunks via callback function
- Displays progress bar during download (via tqdm)

#### Side Effects
- Creates file at `local_path`
- Overwrites existing file if present

#### Test Reference
`tests/test_download_file.py::test_download_file_characterization`

---

### `main()`

```python
def main(destination: Path) -> None
```

Downloads all CNEFE data files from IBGE FTP server.

#### Parameters
- `destination` (Path): Local directory where files will be saved

#### Behavior
- Connects to `ftp.ibge.gov.br`
- Changes to CNEFE CSV directory
- Downloads three types of files:
  1. Dictionary file: `Dicionario_CNEFE_Censo_2022.xls`
  2. All ZIP files from `UF/` directory (obtained via `ftp.nlst("UF")`)
  3. Each file is downloaded only if not already present in destination
- Skips files that already exist locally (checked by filename)

#### Side Effects
- Creates `destination` directory if it doesn't exist
- Creates subdirectories matching FTP structure
- Downloads multiple files to filesystem

#### Network Dependencies
- Requires internet connection
- Connects to `ftp.ibge.gov.br`
- Timeout: 60 seconds

#### Test Reference
`tests/test_download_file.py::test_main_characterization`

---

## `scripts/extract.py`

### `main()`

```python
def main(source: Path, destination: Path, extension: str = None) -> None
```

Extracts files from ZIP archives filtered by extension.

#### Parameters
- `source` (Path): Directory containing ZIP files (searched recursively)
- `destination` (Path): Directory where extracted files will be saved
- `extension` (str, optional): File extension to extract (e.g., `'.csv'`, `'.txt'`)

#### Behavior
- Recursively finds all `*.zip` files in `source`
- For each ZIP file:
  - Opens and reads file list
  - Filters files matching `extension` (case-insensitive comparison)
  - Skips files already present in `destination` (checked by filename)
  - Extracts only matching files
- Continues processing other ZIPs if one is corrupted (`BadZipFile`)

#### Side Effects
- Creates `destination` directory if it doesn't exist
- Extracts files to `destination`
- Prints error message for corrupted ZIP files

#### Example
```python
# Only extracts .csv files, ignores .txt files in same ZIP
main(Path("data/raw"), Path("data/extracted"), extension='.csv')
```

#### Error Handling
- Catches `BadZipFile` exceptions
- Logs corrupted files to stdout
- Continues processing remaining files

#### Test Reference
`tests/test_extract_file.py::test_main_extraction_real_zip`

---

## `scripts/process_metadata.py`

### `main()`

```python
def main(source: Path, output_dir: Path) -> None
```

Processes territorial metadata Excel files into JSON mapping files.

#### Parameters
- `source` (Path): Directory containing IBGE Excel metadata files
- `output_dir` (Path): Directory where JSON mapping files will be saved

#### Behavior
- Reads three Excel files from `source`:
  - `RELATORIO_DTB_BRASIL_2024_MUNICIPIOS.xls`
  - `RELATORIO_DTB_BRASIL_2024_DISTRITOS.xls`
  - `RELATORIO_DTB_BRASIL_2024_SUBDISTRITOS.xls`
- Skips first 6 rows (HEADER_POS = 6) when reading Excel files
- Removes duplicate entries from each dataset
- Creates four JSON mapping files:
  1. `state_mapping.json` - UF code → state name
  2. `municipality_mapping.json` - municipality code → municipality name
  3. `distrital_mapping.json` - district code → district name
  4. `subdistrital_mapping.json` - subdistrict code → subdistrict name

#### Output Format
- JSON files with simple key-value structure: `{"code": "name"}`
- UTF-8 encoding with `ensure_ascii=False`

#### Side Effects
- Creates `output_dir` directory if it doesn't exist
- Creates 4 JSON files in `output_dir`
- Prints progress messages to stdout

#### Column Mappings

**States** (from `RELATORIO_DTB_BRASIL_2024_MUNICIPIOS.xls`):
- Key: `UF` column
- Value: `Nome_UF` column

**Municipalities** (from `RELATORIO_DTB_BRASIL_2024_MUNICIPIOS.xls`):
- Key: `Código Município Completo` column
- Value: `Nome_Município` column

**Districts** (from `RELATORIO_DTB_BRASIL_2024_DISTRITOS.xls`):
- Key: `Código de Distrito Completo` column
- Value: `Nome_Distrito` column

**Subdistricts** (from `RELATORIO_DTB_BRASIL_2024_SUBDISTRITOS.xls`):
- Key: `Código de Subdistrito Completo` column
- Value: `Nome_Subdistrito` column

#### Test Reference
`tests/test_process_metadata.py::test_main_characterization_patched`

---

## `scripts/process_addresses.py`

### `load_mappings()`

```python
def load_mappings(metadata: Path) -> Dict[str, Dict[str, str]]
```

Loads all territorial mapping files from metadata directory.

#### Parameters
- `metadata` (Path): Directory containing JSON mapping files

#### Returns
- `Dict[str, Dict[str, str]]`: Dictionary with keys `"state"`, `"municipality"`, `"distrital"`, `"subdistrital"`, each containing code→name mappings

#### Behavior
- Reads 4 JSON files:
  - `state_mapping.json`
  - `municipality_mapping.json`
  - `distrital_mapping.json`
  - `subdistrital_mapping.json`
- Returns nested dictionary structure

#### Raises
- `FileNotFoundError`: If any mapping file is missing
- `JSONDecodeError`: If any mapping file is invalid JSON

---

### `process_chunk()`

```python
def process_chunk(df: pd.DataFrame, mappings: Dict[str, Dict[str, str]]) -> pd.DataFrame
```

Processes a single chunk of address data, applying transformations and mappings.

#### Parameters
- `df` (pd.DataFrame): Chunk of raw address data
- `mappings` (Dict[str, Dict[str, str]]): Territorial code→name mappings

#### Returns
- `pd.DataFrame`: Transformed and cleaned address data

#### Behavior

**Column Mappings Applied:**
- `COD_UF` → `ESTADO` (mapped to state name)
- `COD_MUNICIPIO` → `MUNICIPIO` (mapped to municipality name)
- `COD_DISTRITO` → `DISTRITO` (mapped to district name)
- `COD_SUBDISTRITO` → `SUBDISTRITO` (mapped to subdistrict name)

**Complement Field Construction:**
- Combines `NOM_COMP_ELEM1` and `VAL_COMP_ELEM1`
- Fills null values with empty strings
- Joins with spaces and normalizes whitespace
- Result stored in `COMPLEMENTO` column

**Address Number Special Handling:**
- When `DSC_MODIFICADOR == "SN"` (sem número):
  - Replaces `NUM_ENDERECO` with `"SN"`
  - Original number value is discarded

**Output Columns (in order):**
1. `ID_ENDERECO` (from `COD_UNICO_ENDERECO`)
2. `ESTADO` (from mapped `COD_UF`)
3. `MUNICIPIO` (from mapped `COD_MUNICIPIO`)
4. `DISTRITO` (from mapped `COD_DISTRITO`)
5. `SUBDISTRITO` (from mapped `COD_SUBDISTRITO`)
6. `BAIRRO` (from `DSC_LOCALIDADE`)
7. `CEP`
8. `TIPO_LOGRADOURO` (from `NOM_TIPO_SEGLOGR`)
9. `RUA` (from `NOM_SEGLOGR`)
10. `NUMERO` (from `NUM_ENDERECO`)
11. `COMPLEMENTO` (constructed)
12. `LATITUDE`
13. `LONGITUDE`

#### Examples

**Complement Construction:**
```python
# Input: NOM_COMP_ELEM1="A", VAL_COMP_ELEM1="X"
# Output: COMPLEMENTO="A X"

# Input: NOM_COMP_ELEM1="B", VAL_COMP_ELEM1=None
# Output: COMPLEMENTO="B"

# Input: NOM_COMP_ELEM1=None, VAL_COMP_ELEM1=None
# Output: COMPLEMENTO=""
```

**Address Number Handling:**
```python
# Input: NUM_ENDERECO="100", DSC_MODIFICADOR="SN"
# Output: NUMERO="SN"

# Input: NUM_ENDERECO="100", DSC_MODIFICADOR=""
# Output: NUMERO="100"
```

---

### `process_file()`

```python
def process_file(filepath: Path, destination: Path, mappings: Dict[str, Dict[str, str]]) -> None
```

Processes a single CSV file in chunks and saves results.

#### Parameters
- `filepath` (Path): Path to input CSV file
- `destination` (Path): Directory where output CSV will be saved
- `mappings` (Dict[str, Dict[str, str]]): Territorial mappings

#### Behavior
- Reads CSV in chunks of 250,000 rows (CHUNKSIZE constant)
- Uses semicolon (`;`) as separator
- Processes only specific columns (defined in COLUMNS constant)
- Applies data type constraints (defined in DTYPES constant)
- Writes output incrementally:
  - First chunk: writes with headers
  - Subsequent chunks: appends without headers
- Output file has same name as input file
- Displays progress bar showing chunk progress

#### Side Effects
- Creates or overwrites CSV file in `destination`
- Writes data incrementally (append mode after first chunk)

#### Memory Management
- Uses chunked reading to handle large files
- Processes 250,000 rows at a time
- Does not load entire file into memory

---

### `main()`

```python
def main(source: Path, metadata: Path, destination: Path) -> None
```

Main pipeline for processing multiple address CSV files.

#### Parameters
- `source` (Path): Directory containing extracted CSV address files
- `metadata` (Path): Directory containing JSON mapping files
- `destination` (Path): Directory where processed CSV files will be saved

#### Behavior
- Loads all territorial mappings from `metadata` directory
- Finds all `*.csv` files in `source` (recursively)
- Sorts files alphabetically
- Processes each file using `process_file()`
- Displays overall progress bar across all files

#### Side Effects
- Creates `destination` directory if it doesn't exist
- Creates processed CSV files in `destination`
- Prints progress information to stdout

#### Input Requirements
- CSV files must use semicolon (`;`) separator
- Must contain required columns (see COLUMNS constant)

#### Performance Characteristics
- Chunk size: 250,000 rows per chunk
- Memory usage: O(chunk_size), not O(file_size)
- Processing is sequential (one file at a time)

#### Test Reference
`tests/test_process_addresses.py::test_main_characterization`

---

## Constants Reference

### `scripts/process_addresses.py`

```python
CHUNKSIZE = 250_000  # Rows per chunk for memory management

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
```

### `scripts/download.py`

```python
FTP_HOST = "ftp.ibge.gov.br"
FTP_DIR = "/Cadastro_Nacional_de_Enderecos_para_Fins_Estatisticos/Censo_Demografico_2022/Arquivos_CNEFE/CSV"
DICTIONARY_PATH = "Dicionario_CNEFE_Censo_2022.xls"
ADDRESSES_PATH = "UF"
CHUNK_SIZE = 1024 * 1024 * 100  # 100 MB
```

### `scripts/process_metadata.py`

```python
HEADER_POS = 6  # Row number where headers start in Excel files

STATE_MUNICIPALITY_FILE = "RELATORIO_DTB_BRASIL_2024_MUNICIPIOS.xls"
DISTRITAL_FILE = "RELATORIO_DTB_BRASIL_2024_DISTRITOS.xls"
SUBDISTRITAL_FILE = "RELATORIO_DTB_BRASIL_2024_SUBDISTRITOS.xls"
```

---

## Testing Notes

All documented behavior is verified by characterization tests in the `tests/` directory. Tests use temporary directories and mock data to ensure behavior is consistent across refactoring efforts.

**Test Coverage**: >80% across all modules (configured in `pyproject.toml`)

**Test Execution**:
```bash
uv run pytest --cov=scripts --cov-report=xml:coverage.xml
```

---

## See Also

- [README.md](../README.md) - Project overview and usage instructions
- [pyproject.toml](../pyproject.toml) - Project configuration and dependencies
- [Makefile](../Makefile) - Pipeline execution commands
