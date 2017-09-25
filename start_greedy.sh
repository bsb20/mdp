#! /bin/bash

lambd_1=${1:-5}
lambd_2=${2:-5}
dirname="greedy_${lambd_1}_${lambd_2}"

if [[ ! -d $dirname ]]
then
    mkdir $dirname
fi

for p1 in 1 2 3 4 5 6 7 8 9
do
    for p2 in 1 2 3 4 5 6 7 8 9
    do
        if [[ $p1 -lt $p2 ]]
        then
            sem -j+0 --id "greedy" -u "python -u parallel_greedy.py .$p1 .$p2 $lambd_1 $lambd_2" > ${dirname}/greedy_${p1}_${p2}.txt
        else
            echo "skipping $p1 $p2"
        fi
    done
done
sem --wait --id "greedy"
