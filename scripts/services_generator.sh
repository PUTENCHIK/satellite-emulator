#!/bin/bash

# Reading content of template of daemons
template=$(<services/service_template)

user="$(whoami)";
path="$(pwd)";
stations=("$@")

sudo mkdir -p /etc/systemd/system/

for station in "${stations[@]}"; do
	# Getting name of station
#	station=$(basename "$dir")
	
	echo "Arg: $station";

	# If necessary daemon already exists, iteration will be skip
	if ! [[ -d "$path/files/$station" ]]; then
		echo "Directory of station $station doesn't exist";
		continue;
	fi
	
	if [[ -f "/etc/systemd/system/$station.service" ]]; then
		echo "Init file of station $station already exists"
		continue;
	fi
	
	# Selection of date from filename
#	sudo mkdir -p /etc/systemd/system/

	# Inserting         
	echo "${template//\$\{path\}/$path}" | \
	sed "s/\$receiver/$station/g" | \
	sed "s/\$user/$user/g" | sudo tee "/etc/systemd/system/$station.service" > /dev/null

	sudo systemctl daemon-reload
#	sudo systemctl enable "$station.service"
	sudo systemctl start "$station.service"
done
