#!/bin/bash

if ls ./config/; then
    for entry in $(ls ./config/)
    do
        python3 evaluate.py -name=$entry
    done
else
    echo "No entry in ./config"
fi
