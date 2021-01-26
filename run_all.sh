#!/bin/bash

start=`date +%s`

if ls ./config/; then
    for entry in $(ls ./config/)
    do
        if [ $entry != "README.md" ]; then
            echo "python3 evaluate.py -name=$entry > ./log/${entry}.log"
            python3 evaluate.py -name=$entry > ./log/${entry}.log &
        fi
    done
else
    echo "No entry in ./config"
fi

end=`date +%s`
runtime=$((end-start))

echo ""
echo "Total runtime: $runtime"
echo ""