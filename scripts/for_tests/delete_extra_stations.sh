#!/bin/bash


# Checking first arg is number
reg='^[0-9]+$';
if ! [[ $1 =~ $reg ]]; then
        echo 'First argument must be number';
	exit 1;
fi

# Checking first arg is more than 0
if [[ $1 == 0 ]]; then
	echo 'First argument must be more than 0';
	exit 2;
fi

i=1;
limit=$1;

for station in files/*/; do
	# If script already skipped necessery amount of folders, it will remove others
	if [[ $i -gt $limit ]]; then
		echo "Removing directory $i) $station";
		rm -rf $station;
	fi
	((i++));
	
done
