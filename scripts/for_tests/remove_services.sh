#!/bin/bash

for dir in files/*/; do
        # Getting name of station
        station=$(basename "$dir")

	if [[ -f "/etc/systemd/system/$station.service" ]]; then
		echo "Removing: $station.service";
		sudo systemctl stop $station.service;
                sudo rm -f "/etc/systemd/system/$station.service";
        fi

	sudo systemctl daemon-reload;
done
