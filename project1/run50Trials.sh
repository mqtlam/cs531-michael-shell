#!/bin/bash

if [ ! -d "trials" ]; then
	mkdir trials
fi

for num in `seq 50`; do
	python runAgent.py 2 > "trials/$num.txt"
done
