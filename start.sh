#! /bin/bash
lambd_1=${1:-5}
lambd_2=${2:-5}
dirname="opt_${lambd_1}_${lambd_2}"

if [[ ! -d $dirname ]]
then
    mkdir $dirname
fi

for p1 in 1 2 3 4 5 6 7 8 9
do
    for p2 in 1 2 3 4 5 6 7 8 9
    do
        if [[ $p1 -le $p2 && ! -e "${dirname}/opt_${p1}_${p2}.txt" ]]
        then
            sem -j+0 --id "mdp" -u "python -u parallel_mdp.py .$p1 .$p2 $lambd_1 $lambd_2" > ${dirname}/opt_${p1}_${p2}.txt
        else
            echo "skipping $p1 $p2"
        fi
    done
done
sem --wait --id "mdp"

#./start_greedy.sh $lambd_1 $lambd_2
