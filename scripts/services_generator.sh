#!/bin/bash

# Reading content of template of daemons
template=$(<services/service_template)

user="$(whoami)";
path="$(pwd)";

for dir in files/*/; do
	# Getting name of station
	station=$(basename "$dir")
	
	# If necessary daemon already exists, iteration will be skip
	if [[ -f "/etc/systemd/system/$station.service" ]]; then
		continue
	fi
	
	# Taking first RINEX file from station directory
	rnx_file=$(find "$dir" -name '*.rnx' | sort)
	rnx_file=${rnx_file[0]}
    
	if [[ -n $rnx_file ]]; then
		# Selection of date from filename
		date=$(basename "$rnx_file")
        
		sudo mkdir -p /etc/systemd/system/

		# Inserting         
		echo "${template//\$\{path\}/$path}" | \
		sed "s/\$receiver/$station/g" | \
		sed "s/\$date/$date/g" | \
		sed "s/\$user/$user/g" | sudo tee "/etc/systemd/system/$station.service" > /dev/null

		sudo systemctl daemon-reload
		sudo systemctl enable "$station.service"
	fi
done
