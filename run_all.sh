#!/bin/bash

start=`date +%s`

if ls ./config/; then
    for entry in $(ls ./config/)
    do
        echo "python3 evaluate.py -name=$entry"
        python3 evaluate.py -name=$entry &
    done
else
    echo "No entry in ./config"
fi

end=`date +%s`
runtime=$((end-start))

echo ""
echo "Total runtime: $runtime"
echo ""