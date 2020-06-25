#!/bin/bash

PacmanGame="Pacman"

while read -r line; do
	name=$(echo "$line" | rev | cut -d "/" -f1)
	if (("$name" == "$PacmanGame")); then
		cd $line && python3 main.py 
		break
	fi
done < <(find 2> /dev/null ~ -d -name "Pacman")
