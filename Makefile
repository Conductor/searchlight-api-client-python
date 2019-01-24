.PHONY: help test nosetests install build-source pypi-upload

help:
	# Commands
	# make help		              - Shows this message
	#
	# Dev commands:
	# make install                        - Install requirements.txt
	# make test                           - Builds all required images
	#

test: nosetests

pypi-upload:
	twine upload dist/*

build-source:
	@python3 setup.py sdist

nosetests:
	@python3 setup.py nosetests

install:
	@pip3 install -r requirements.txt
