#! /bin/bash

lambd_1=${1:-4}
lambd_2=${2:-4}
p1=${3:-6}
p2=$p1

dirname="greedy_${lambd_1}_${lambd_2}"

if [[ ! -d $dirname ]]
then
    mkdir $dirname
fi

for mu_1 in 1 2 4 8 16 32 64 128 256 512 1024
do
    for mu_2 in 1 2 4 8 16 32 64 128 256 512 1024
    do
        if [[ $mu_1 -lt $mu_2 ]]
        then
            sem -j+0 --id "greedy" -u "python -u parallel_greedy.py .$p1 .$p2 $lambd_1 $lambd_2 $mu_1 $mu_2" > ${dirname}/greedy_mu_${mu_1}_${mu_2}.txt
        else
            echo "skipping $mu_1 $mu_2"
        fi
    done
done
sem --wait --id "greedy"
