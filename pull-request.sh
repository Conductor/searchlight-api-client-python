#!/bin/bash

if make test 
then
    echo "Verified tests pass."
else
    echo "Error: unable to verify tests passed."
    exit 1
fi
