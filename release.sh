#!/bin/bash

if make test
then
    echo "Verified tests pass."
else
    echo "Error: unable to verify tests passed."
    exit 1
fi

# publish a new version (will result in an error if VERSION does not have a new version)
make docker-release upload-k8s-release
exit
