#!/bin/bash

set -e
set -o noclobber

alias cp="cp -i"
unalias cp

technode="32nm_rvt"
# technode="45nm_rvt"

echo "Process technode: $technode"

cp -R src_sv ./$technode

cd $technode
for subdir in $(ls -d */)
do
    subdir="${subdir%/}"
    subdir="${subdir%/}"
    subdir="${subdir%/}"
    echo "Process dir: $technode/$subdir"

    cd $subdir
    for subsubdir in $(ls -d */)
    do
        subsubdir="${subsubdir%/}"
        subsubdir="${subsubdir%/}"
        subsubdir="${subsubdir%/}"
        cd $subsubdir
        echo "Process dir: $technode/$subdir/$subsubdir"
        rm -rf syn* .syn*
        cp ../../../syn_* .
        cp ../../../synopsys_dc.setup_$technode .synopsys_dc.setup
        source syn_run.sh
        cd ..
    done
    cd ..
done
cd ..
