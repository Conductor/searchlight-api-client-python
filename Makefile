.PHONY: help test nosetests intall

help:
	# Commands
	# make help		              - Shows this message
	#
	# Dev commands:
	# make install                        - Install requirements.txt
	# make test                           - Builds all required images
	#

test: nosetests

nosetests:
	@python setup.py nosetests

install:
	@pip install -r requirements.txt
