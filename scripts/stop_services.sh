#!/bin/bash


me=$(basename "$0");
scripts/logger.sh "$me" 'info' "Called $me script"

stations=("$@")

for station in "${stations[@]}"; do
	# Checking daemon's file exists
        if ! [[ -f "/etc/systemd/system/$station.service" ]]; then
                scripts/logger.sh "$me" 'warning' "Config file of station $station doesn't exist"
                continue;
        fi

	sudo systemctl daemon-reload
        sudo systemctl stop "$station.service"

	scripts/logger.sh "$me" 'debug' "Station $station's daemon stopped"
done


SCRIPT_PATH="$(pwd)/scripts/crontab.sh"
crontab -l | grep -v "$SCRIPT_PATH" | crontab -
scripts/logger.sh "$me" 'debug' "Removed rows in crontab.sh which will restart daemons"

if ! [[ -f "/etc/systemd/system/subscriber.service" ]]; then
	scripts/logger.sh "$me" 'warning' "Config file of subscriber' daemon doesn't exist"
else
	sudo systemctl stop "subscriber.service"
	scripts/logger.sh "$me" 'debug' "Subscriber's daemon was stopped"
fi
