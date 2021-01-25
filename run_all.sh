#!/bin/bash

start=`date +%s`

if ls ./config/; then
    for entry in $(ls ./config/)
    do
        echo "python3 evaluate.py -name=$entry > ${entry}.log"
        python3 evaluate.py -name=$entry > ${entry}.log &
    done
else
    echo "No entry in ./config"
fi

end=`date +%s`
runtime=$((end-start))

echo ""
echo "Total runtime: $runtime"
echo ""