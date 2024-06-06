.DEFAULT_GOAL := default
#################### PACKAGE ACTIONS ###################

install_package:
	@pip install -e .

reinstall_package:
	@pip uninstall -y tfl_status || :
	@pip install -e .

check_status:
	python -c 'from backend.main.interface import run_app; run_app()'

################## CLEANING ACTIONS ####################

clean:
	@rm -rf build dist tfl_status.egg-info

clean_cache:
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -delete

clean_all: clean clean_cache

clean_data:
	@rm raw_data/*.csv
