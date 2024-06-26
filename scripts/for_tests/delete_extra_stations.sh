#!/bin/bash


me=$(basename "$0");
scripts/logger.sh "$me" 'info' "Called $me script"

# Checking first arg is number
reg='^[0-9]+$';
if ! [[ $1 =~ $reg ]]; then
	scripts/logger.sh "$me" 'error' "First argument isn/'t number"
        echo 'First argument must be number';
	exit 1;
fi

# Checking first arg is more than 0
if [[ $1 == 0 ]]; then
	scripts/logger.sh "$me" 'error' "First argument is less than 0"
	echo 'First argument must be more than 0';
	exit 2;
fi

i=1;
limit=$1;

for station in files/*/; do
	# If script already skipped necessery amount of folders, it will remove others
	if [[ $i -gt $limit ]]; then
		scripts/logger.sh "$me" 'debug' "Removing directory $(basename $station)"
		echo "Removing directory $station";
		rm -rf $station;
	else
		scripts/logger.sh "$me" 'debug' "Saving directory $(basename $station)"
		echo "Saving directory $station";
	fi
	((i++));
	
done
