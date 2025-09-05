.PHONY: clean download extract

PYTHON_INTERPRETER = python

ifeq (,$(shell $(PYTHON_INTERPRETER) --version))
$(error "Python is not installed!")
endif

download:
	@$(PYTHON_INTERPRETER) scripts/download.py data/raw

extract:
	@$(PYTHON_INTERPRETER) scripts/extract.py data/raw data/extracted

## Delete all compiled Python files
clean:
	@find . -type f -name "*.py[co]" -delete
	@find . -type d -name "__pycache__" -delete
	@find . -type d -name ".tox" -exec rm -r "{}" +
	@find . -type d -name ".pytest_cache" -exec rm -r "{}" +