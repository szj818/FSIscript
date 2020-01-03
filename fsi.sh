#!/bin/bash

echo "--- Starting job at:`date`"

export NPA=1
export NP=2
export NPF=$((NP))
export NODES=$(hostname)
export FLUID='Solution'
export STRUCT='Solution 1'

"$AWP_ROOT195/SystemCoupling/bin/systemcoupling" -R fsi.py 

echo "--- Job finished at:`date`"
