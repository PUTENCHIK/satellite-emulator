#!/bin/bash


me=$(basename "$0");
scripts/logger.sh "$me" 'info' "Called $me script"

# Reading content of template of daemons
template=$(<templates/subscriber_template)

user="$(whoami)";
path="$(pwd)";

if [[ -f "/etc/systemd/system/subscriber.service" ]]; then
	scripts/logger.sh "$me" 'debug' "subscriber.service already exists: restarting daemon"
	sudo systemctl start "subscriber.service"
	exit 1;
fi

sudo mkdir -p /etc/systemd/system/

echo "${template//\$\{path\}/$path}" | \
sed "s/\$user/$user/g" | sudo tee "/etc/systemd/system/subscriber.service" > /dev/null

scripts/logger.sh "$me" 'debug' "subscriber.service was created: starting daemon"
sudo systemctl daemon-reload
sudo systemctl enable "subscriber.service"
sudo systemctl start "subscriber.service"
