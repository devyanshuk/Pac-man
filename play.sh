#!/bin/bash

PacmanGame="Pac-man"

while read -r line; do
	name=$(echo "$line" | rev | cut -d "/" -f1)
	name=$(echo "$name" | rev)
	if (("$name" == "$PacmanGame")); then
		pip install pygame
		cd $line && python3 main.py 
		break
	fi
done < <(find 2> /dev/null ~ -d -name "Pac-man")
