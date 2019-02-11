#!/bin/bash

if make test
then
    echo "Verified tests pass."
    export TWINE_USERNAME=$PYPI_DEPLOY_USER
    export TWINE_PASSWORD=$PYPI_DEPLOY_PASS
else
    echo "Error: unable to verify tests passed."
    exit 1
fi

# publish a new version (will result in an error if VERSION does not have a new version)
make build upload
exit
