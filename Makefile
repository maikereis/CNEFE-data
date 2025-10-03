PYTHON_INTERPRETER = python

ifeq (,$(shell $(PYTHON_INTERPRETER) --version))
$(error "Python is not installed!")
endif

.PHONY: all clean download metadata extract extract_metadata process_metadata process_addresses

# Run the full pipeline
all: download metadata extract extract_metadata process_metadata process_addresses

download:
	@$(PYTHON_INTERPRETER) scripts/download.py data/raw

metadata:
	@$(PYTHON_INTERPRETER) scripts/metadata.py data/metadata

extract:
	@$(PYTHON_INTERPRETER) scripts/extract.py data/raw data/extracted/addresses extension='.csv'

extract_metadata:
	@$(PYTHON_INTERPRETER) scripts/extract.py data/metadata data/extracted/metadata extension='.xls'

process_metadata:
	@$(PYTHON_INTERPRETER) scripts/process_metadata.py data/extracted/metadata data/processed/metadata

process_addresses:
	@$(PYTHON_INTERPRETER) scripts/process_addresses.py data/extracted/addresses data/processed/metadata data/processed/addresses

## Delete all compiled Python files
clean:
	@find . -type f -name "*.py[co]" -delete
	@find . -type d -name "__pycache__" -delete
	@find . -type d -name ".tox" -exec rm -r "{}" +
	@find . -type d -name ".pytest_cache" -exec rm -r "{}" +
