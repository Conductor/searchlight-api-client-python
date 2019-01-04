.PHONY: help test nosetests intall

help:
	# Commands
	# make help		              - Shows this message
	#
	# Dev commands:
	# make install                        - Install requirements.txt
	# make test                           - Builds all required images
	#

test: install nosetests

nosetests:
	@python setup.py nosetests

install:
	@apt-get install -y python-setuptools
	@pip install -r requirements.txt
