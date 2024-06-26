#!/bin/bash


function log {
	datetime=$(date '+%Y-%m-%d %H:%M:%S,%3N');
	echo "$template" | \
	sed "s/\$datetime/$datetime/g" | \
	sed "s/\$name/$1/g" | \
	sed "s/\$level/$2/g" | \
	sed "s/\$message/$3/g" >> "$path/logs.log";
}


template=$(<templates/logger_string_template);
path=$(pwd);

name=$1;
level=$(echo "$2" | tr a-z A-Z);
message=$3;

#echo "Args: $name | $level | $message"

levels=("DEBUG" "INFO" "WARNING" "ERROR");

if [[ ${levels[@]} =~ $level ]]; then
	log "$name" "$level" "$message";
else
	log "logger.sh" "ERROR" "Got bad logger's level: $level";
fi
