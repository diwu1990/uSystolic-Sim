#!/bin/bash

start=`date +%s`

if ls ./config/; then
    for entry in $(ls ./config/)
    do
        if [ $entry != "README.md" ]; then
            if [ ! -f "./outputs/$entry/simArchOut/${entry}_mac_util.csv" ]; then
                echo "./outputs/$entry/simArchOut/${entry}_mac_util.csv does not exist!"
            fi

            if [ ! -f "./outputs/$entry/simEffOut/${entry}_area.csv" ]; then
                echo "./outputs/$entry/simEffOut/${entry}_area.csv does not exist!"
            fi
            if [ ! -f "./outputs/$entry/simEffOut/${entry}_energy.csv" ]; then
                echo "./outputs/$entry/simEffOut/${entry}_energy.csv does not exist!"
            fi
            if [ ! -f "./outputs/$entry/simEffOut/${entry}_power.csv" ]; then
                echo "./outputs/$entry/simEffOut/${entry}_power.csv does not exist!"
            fi
            if [ ! -f "./outputs/$entry/simHwOut/${entry}_detail_ideal.csv" ]; then
                echo "./outputs/$entry/simHwOut/${entry}_detail_ideal.csv does not exist!"
            fi
            if [ ! -f "./outputs/$entry/simHwOut/${entry}_avg_bw_ideal.csv" ]; then
                echo "./outputs/$entry/simHwOut/${entry}_avg_bw_ideal.csv does not exist!"
            fi
            if [ ! -f "./outputs/$entry/simHwOut/${entry}_detail_real.csv" ]; then
                echo "./outputs/$entry/simHwOut/${entry}_detail_real.csv does not exist!"
            fi
            if [ ! -f "./outputs/$entry/simHwOut/${entry}_avg_bw_real.csv" ]; then
                echo "./outputs/$entry/simHwOut/${entry}_avg_bw_real.csv does not exist!"
            fi
        fi
    done
else
    echo "No entry in ./config"
fi

end=`date +%s`
runtime=$((end-start))

echo ""
echo "All checked!"
echo ""
echo "Total runtime: $runtime"
echo ""