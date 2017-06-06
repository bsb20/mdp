#! /bin/bash

for p1 in 1 2 3 4 5 6 7 8 9
do
    for p2 in 1 2 3 4 5 6 7 8 9
    do
        if [[ $p1 -lt $p2 ]]
        then
            sem -j+0 --id "mdp" -u "python -u parallel_mdp.py .$p1 .$p2" > opt_7_7/${p1}_${p2}.txt
        else
            echo "skipping $p1 $p2"
        fi
    done
done
sem --wait --id "mdp"
