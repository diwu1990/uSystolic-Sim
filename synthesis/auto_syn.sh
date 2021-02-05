#!/bin/bash

set -e
set -o noclobber

alias cp="cp -i"
unalias cp

for dir in $(ls -d */)
do
    dir="${dir%/}"
    dir="${dir%/}"
    dir="${dir%/}"
    echo "Process technode: $dir"

    cd $dir
    for subdir in $(ls -d */)
    do
        subdir="${subdir%/}"
        subdir="${subdir%/}"
        subdir="${subdir%/}"
        echo "Process dir: $dir/$subdir"

        cd $subdir
        for subsubdir in $(ls -d */)
        do
            subsubdir="${subsubdir%/}"
            subsubdir="${subsubdir%/}"
            subsubdir="${subsubdir%/}"
            cd $subsubdir
            echo "Process dir: $dir/$subdir/$subsubdir"
            rm -rf syn* .syn*
            cp ../../../syn_* .
            cp ../../../synopsys_dc.setup_$dir .synopsys_dc.setup
            source syn_run.sh
            cd ..
        done
        cd ..
    done
    cd ..
done

# # rename *.v to *.sv
# echo ""
# echo "Check *.v files:"
# if ls *.$vsuff; then
#     echo "Rename $dut to ${dut%.$vsuff}.$svsuff"
#     for dut in $(ls *.$vsuff)
#     do
#         mv -f $dut ${dut%.$vsuff}.$svsuff
#     done
# fi

# echo ""
# echo "Synthesize designs in *.sv files:"
# if ls *.$svsuff; then
#     for dut in $(ls *.$svsuff)
#     do
#         dutname="${dut%.*}"
#         echo "Processing design $dutname in $dut..."
#         sed -i "s/dut/$dutname/g" $DCSCRIPT
#         dc_shell -f $DCSCRIPT >| $dutname.rpt
#         sed -i "s/$dutname/dut/g" $DCSCRIPT
#         rm -rf work/ *.vg *.svf
#         echo "    Done"
#     done
# else
#     echo "No design exists."
#     return 0
# fi

# echo ""
# echo "Check potential errors in log:"
# grep -Ri "Error" ./*
# grep -Ri "connected" ./*
# echo ""
# echo "******************************All Done******************************"
# echo ""


