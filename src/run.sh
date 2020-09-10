#! /bin/bash
for fb in 14
do
    python FODPSim.py -diskCap 16 -M 48 -D 169 -S 13 -k 11 -m 2 -fb $fb -dtype 2 -ftype $1 -mtbf 0.5 -percent 0.01
done
