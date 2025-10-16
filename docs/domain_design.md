# CNEFE Domain Design

## Ubiquitous Language

* **Address**: A georeferenced location with administrative divisions
* **Territorial Division**: Hierarchical administrative unit (UF → Municipality → District → Subdistrict)
* **Territorial Codes**: Hierarchical IBGE identifier
* **Address Species**: Classification (residential, commercial, construction, establishment)
* **Address Component**: Parts of address (Street, Number, Complement)
* **CNEFE**: Cadastro Nacional de Endereços para Fins Estatísticos
* **Coordinate**: Geospatial point (latitude, longitude)
* **Establishment Type**: Non-residential category (educational, healthcare, religious, agricultural)
* **Geocoding Level**: Coordinate precision (1=original, 2=modified, 3=estimated, 4=face, 5=locality, 6=sector)
* **Street Type**: Logradouro classification (RUA, AVENIDA, TRAVESSA)
* **PostalCode**: Standardized code for mail delivery and geographic reference
* **Address Modifier**: Special indicator (e.g., "SN" for addresses without numbers)

## Context Map

```
┌──────────────┐
│     IBGE     │  [External System]
│  (Upstream)  │
└──────┬───────┘
       │ [Published Language]
       │ Supplies: Raw CNEFE data via FTP
       ↓
┌──────────────┐
│     Data     │  [Anticorruption Layer]
│ Acquisition  │
└──────┬───────┘
       │ [Customer/Supplier]
       │ Supplies: Cleaned CSVs + JSON mappings
       ↓
┌──────────────┐
│   Address    │  [Core Domain]
│  Processing  │
└──────────────┘
```

## Relationships

* **Customer/Supplier** (IBGE → Data Acquisition): IBGE supplies CNEFE data; Data Acquisition acts as Anticorruption Layer, translating IBGE's complex format into domain-friendly structure

* **Customer/Supplier** (Data Acquisition → Address Processing): Data Acquisition supplies cleaned CSVs and territorial JSON mappings to Address Processing, which enriches and validates addresses according to domain rules

## Processing Pipeline (Domain Operations)

1. **Data Acquisition Context**
   - Download raw files from IBGE FTP
   - Extract ZIP archives
   - Generate territorial mapping JSONs

2. **Address Processing Context**
   - Load territorial mappings (Repository)
   - Read CSV chunks (Infrastructure)
   - For each chunk:
     - Parse raw data → Create Address aggregates
     - Apply AddressEnrichmentService
     - Apply CoordinateValidationService
     - Apply ComplementNormalizationService
     - Validate invariants
     - Persist via AddressRepository
     - Emit AddressEnriched events
   - Emit BatchProcessingCompleted event

## Domain Model

### Aggregates

**Address** (Aggregate Root)
- Identity: `ID_ENDERECO` (unique identifier)
- Contains:
  - `TerritorialDivision` (value object)
  - `Coordinate` (value object)
  - `StreetAddress` (value object)
  - `PostalCode` (value object)
  - `Species` (enum)
  - `GeocodingLevel` (enum)
- Invariants:
  - Must have valid territorial hierarchy (UF → Municipality → District → Subdistrict)
  - Addresses without number must use modifier "SN"
  - Coordinate precision must match geocoding level
  - Species determines required establishment metadata

### Value Objects

**Coordinate**
```python
@dataclass(frozen=True)
class Coordinate:
    latitude: float
    longitude: float
    precision_level: GeocodingLevel
```

**StreetAddress**
```python
@dataclass(frozen=True)
class StreetAddress:
    street_type: str
    street_name: str
    number: str
    modifier: Optional[str]  # SN, S/N.
    complement: str
```

**PostalCode**
```python
@dataclass(frozen=True)
class PostalCode:
    code: str  # Format: XXXXX-XXX
```

**TerritorialDivision**
```python
@dataclass(frozen=True)
class TerritorialDivision:
    uf: str
    municipality: str
    district: str
    subdistrict: str
```

### Enums

**AddressSpecies**
```python
class AddressSpecies(Enum):
    RESIDENTIAL = 1
    COLLECTIVE_DWELLING = 2
    AGRICULTURAL = 3
    EDUCATIONAL = 4
    HEALTHCARE = 5
    OTHER_ESTABLISHMENT = 6
    UNDER_CONSTRUCTION = 7
    RELIGIOUS = 8
```

**GeocodingLevel**
```python
class GeocodingLevel(Enum):
    ORIGINAL = 1
    MODIFIED = 2
    ESTIMATED = 3
    FACE = 4
    LOCALITY = 5
    SECTOR = 6
```

### Domain Services

**AddressEnrichmentService**
- Responsibility: Apply territorial mappings to raw addresses
- Operations:
  - `enrich(raw_address, territorial_mappings) -> Address`
  - Resolves territorial codes to names
  - Normalizes address components

**CoordinateValidationService**
- Responsibility: Validate and classify coordinate precision
- Operations:
  - `validate(coordinate) -> bool`
  - `determine_precision_level(coordinate, metadata) -> GeocodingLevel`

**ComplementNormalizationService**
- Responsibility: Parse and standardize address complements
- Operations:
  - `normalize(elements: List[Tuple[str, str]]) -> str`
  - Combines multiple complement elements
  - Removes redundant whitespace

### Repositories

**AddressRepository**
```python
class AddressRepository(Protocol):
    def save_batch(self, addresses: List[Address]) -> None
    def find_by_id(self, address_id: str) -> Optional[Address]
    def find_by_territorial_division(self, code: TerritorialDivision) -> List[Address]
    def find_by_postal_code(self, postal_code: PostalCode) -> List[Address]
```

**TerritorialMappingRepository**
```python
class TerritorialMappingRepository(Protocol):
    def load_state_mapping(self) -> Dict[str, str]
    def load_municipality_mapping(self) -> Dict[str, str]
    def load_district_mapping(self) -> Dict[str, str]
    def load_subdistrict_mapping(self) -> Dict[str, str]
```

### Domain Events

**AddressEnriched**
```python
@dataclass
class AddressEnriched:
    address_id: str
    territorial_division: TerritorialDivision
    timestamp: datetime
```

**BatchProcessingCompleted**
```python
@dataclass
class BatchProcessingCompleted:
    file_name: str
    total_addresses: int
    timestamp: datetime
```

## Domain Rules (Invariants)

1. **Territorial Hierarchy**: Every address must have complete territorial chain (UF → Municipality → District → Subdistrict)

2. **Number Normalization**: When `DSC_MODIFICADOR == "SN"`, `NUM_ENDERECO` must be set to "SN"

3. **Complement Consolidation**: Multiple complement elements (`NOM_COMP_ELEM*`, `VAL_COMP_ELEM*`) must be merged into single normalized string

4. **Coordinate Precision**: Geocoding level determines data quality expectations:
   - Level 1-3: Individual address precision
   - Level 4-6: Aggregated location precision

5. **Species-Specific Metadata**: Establishment species (4-6, 8) require `DSC_ESTABELECIMENTO` field
