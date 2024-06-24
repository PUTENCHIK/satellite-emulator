#!/bin/bash

# Reading content of template of daemons
template=$(<services/subscriber_template)

user="$(whoami)";
path="$(pwd)";

if [[ -f "/etc/systemd/system/subscriber.service" ]]; then
	exit 1;
fi

sudo mkdir -p /etc/systemd/system/

echo "${template//\$\{path\}/$path}" | \
sed "s/\$user/$user/g" | sudo tee "/etc/systemd/system/subscriber.service" > /dev/null
sudo systemctl daemon-reload
sudo systemctl enable "subscriber.service"
