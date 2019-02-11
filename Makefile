.PHONY: help test nosetests install build-source pypi-upload

help:
	# Commands
	# make help		              - Shows this message
	#
	# Dev commands:
	# make install                        - Installs dependencies in requirements.txt
	# make test                           - Runs unit and integration tests using nosetests
	#
	# Build commands:
	# make build                          - Builds package tar.gz
	# make upload                         - Uploads package to pypi

test:
	@python3.6 setup.py nosetests

upload:
	twine upload dist/*

build:
	@python3.6 setup.py sdist

install:
	@python3.6 -m pip install -r requirements.txt
