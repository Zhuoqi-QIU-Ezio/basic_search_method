#!/bin/sh

python red_bird.py -l $1 -p SearchAgent -a fn=astar,heuristic=$2
