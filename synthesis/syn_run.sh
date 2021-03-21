#!/bin/bash
# this is a shell script to run dc synthesis for all *.sv files in this foler
# note that the *.sv files require identical file and module name

set -e
set -o noclobber


echo ""
echo "***************************Start Synthesis**************************"
# check the existance of dc setup file and dc run script
SETUPFILE=.synopsys_dc.setup
SRCSETUPFILE=synopsys_dc.setup
if [ ! -f $SETUPFILE ]; then
    if [ -f $SRCSETUPFILE ]; then
        mv $SRCSETUPFILE $SETUPFILE
    else
        echo ""
        echo "Design Compiler setup file $SETUPFILE or $SRCSETUPFILE does not exist."
        return 0
    fi
fi

DCSCRIPT=syn_script.tcl
if [ ! -f $DCSCRIPT ]; then
    echo ""
    echo "Design Compiler script $DCSCRIPT does not exist."
    return 0
fi

svsuff=sv
vsuff=v

# rename *.v to *.sv
echo ""
echo "Check *.v files:"
if ls *.$vsuff; then
    echo "Rename $dut to ${dut%.$vsuff}.$svsuff"
    for dut in $(ls *.$vsuff)
    do
        mv -f $dut ${dut%.$vsuff}.$svsuff
    done
fi

echo ""
echo "Synthesize designs in *.sv files:"
if ls *.$svsuff; then
    for dut in $(ls *.$svsuff)
    do
        dutname="${dut%.*}"
        echo "Processing design $dutname in $dut..."
        sed -i "s/dut/$dutname/g" $DCSCRIPT
        dc_shell -f $DCSCRIPT >| $dutname.rpt
        sed -i "s/$dutname/dut/g" $DCSCRIPT
        rm -rf work/ *.vg *.svf
        echo "    Done"
        sleep 10s
    done
else
    echo "No design exists."
    return 0
fi

echo ""
echo "Check potential errors in log:"
grep -Ri "Error" ./*
grep -Ri "connected" ./*
echo ""
echo "******************************All Done******************************"
echo ""


