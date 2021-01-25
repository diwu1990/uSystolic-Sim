#!/bin/bash

if ls ./config/; then
    for entry in $(ls ./config/)
    do
        echo "python3 evaluate.py -name=$entry"
        python3 evaluate.py -name=$entry
    done
else
    echo "No entry in ./config"
fi
