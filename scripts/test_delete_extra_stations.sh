#!/bin/bash


# Checking first arg is number
reg='^{0-9]+$'
if ! [[ $1 =~ $reg ]]; then
	echo "First argument must be number: $1";
	exit 1;
fi

if $1 == 0; then
	echo "First argument must be more than 0";
	exit 2;
fi

i=1;

for station in files/*/; do
	if $i > $1; then
		rm -r $station;
	fi
	((i++));
done
