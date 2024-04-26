.DEFAULT_GOAL := default
#################### PACKAGE ACTIONS ###################
reinstall_package:
	@pip uninstall -y tfl_status || :
	@pip install -e .

check_status:
	python -c 'from main.interface import run_app; run_app()'
