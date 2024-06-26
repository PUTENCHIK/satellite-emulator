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
        sudo systemctl restart "$station.service"

        scripts/logger.sh "$me" 'debug' "Station $station's daemon restarted"
done


scripts/config_crontab.sh
scripts/logger.sh "$me" 'debug' "Added in crontab rows to restart stations' daemons"

if ! [[ -f "/etc/systemd/system/subscriber.service" ]]; then
        scripts/logger.sh "$me" 'warning' "Config file of subscriber' daemon doesn't exist"
else
        sudo systemctl restart "subscriber.service"
        scripts/logger.sh "$me" 'debug' "Subscriber's daemon was stopped"
fi
