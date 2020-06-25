#!/bin/bash

PacmanGame="Pac-man"
brew install coreutils
DIR="$(dirname "$(greadlink -f "$0")")"

while read -r line; do
	name=$(echo "$line" | rev | cut -d "/" -f1)
	name=$(echo "$name" | rev)
	if (("$name" == "$PacmanGame")); then
		echo -e "alias pac-man='cd "$DIR" && python3 main.py'\n$(cat ~/.bash_profile)" > ~/.bash_profile
		pip install pygame
		cd $line && python3 main.py 
		break
	fi
done < <(find 2> /dev/null ~ -d -name "Pac-man")
