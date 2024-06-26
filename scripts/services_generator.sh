#!/bin/bash


me=$(basename "$0");
scripts/logger.sh "$me" 'info' "Called $me script"

# Reading content of template of daemons
template=$(<templates/service_template)

user="$(whoami)";
path="$(pwd)";
stations=("$@")

sudo mkdir -p /etc/systemd/system/

for station in "${stations[@]}"; do
	# Checkimg directory of station exists
	if ! [[ -d "$path/files/$station" ]]; then
		scripts/logger.sh "$me" 'warning' "Directory of station $station doesn't exist" 
		continue;
	fi
	
	# Checking daemon's file already exists
	if [[ -f "/etc/systemd/system/$station.service" ]]; then
		scripts/logger.sh "$me" 'debug' "Config file of station $station already exists"
		sudo systemctl start "$station.service"
		continue;
	fi

	# Inserting         
	echo "${template//\$\{path\}/$path}" | \
	sed "s/\$receiver/$station/g" | \
	sed "s/\$user/$user/g" | sudo tee "/etc/systemd/system/$station.service" > /dev/null

	sudo systemctl daemon-reload
	sudo systemctl start "$station.service"
	#sudo systemctl enable "$station.service"
	scripts/logger.sh "$me" 'debug' "Station $station's daemon created and started"
done
