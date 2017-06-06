#! /bin/bash

for p1 in 1 2 3 4 5 6 7 8 9
do
    for p2 in 1 2 3 4 5 6 7 8 9
    do
        if [[ $p1 -lt $p2 ]]
        then
            python -u parallel_greedy.py .$p1 .$p2 > greedy_7_7/greedy_${p1}_${p2}.txt
        else
            echo "skipping $p1 $p2"
        fi
    done
done
