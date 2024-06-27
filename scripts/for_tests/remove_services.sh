#!/bin/bash


me=$(basename "$0");
scripts/logger.sh "$me" 'info' "Called $me script"

# Removing subscriber's daemon
if [[ -f "/etc/systemd/system/subscriber.service" ]]; then
	sudo systemctl stop "subscriber.service";
	sudo systemctl disable "subscriber.service";
	sudo rm -f "/etc/systemd/system/subscriber.service";

	scripts/logger.sh "$me" 'debug' 'subscriber.service removed'
fi

# Removing subscriber's daemon
if [[ -f "/etc/systemd/system/file_preparer.service" ]]; then
        sudo systemctl stop "file_preparer.service";
        sudo systemctl disable "file_preparer.service";
        sudo rm -f "/etc/systemd/system/file_preparer.service";

        scripts/logger.sh "$me" 'debug' 'file_preparer.service removed'
fi

# Removing stations' daemons
for dir in files/*/; do
        station=$(basename "$dir")

	if [[ -f "/etc/systemd/system/$station.service" ]]; then
		echo "Removing: $station.service";
		sudo systemctl stop "$station.service";
		sudo systemctl disable "$station.service";
                sudo rm -f "/etc/systemd/system/$station.service";

		scripts/logger.sh "$me" 'debug' "$station.service removed"
        fi
done

sudo systemctl daemon-reload;
