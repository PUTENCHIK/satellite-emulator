#!/bin/bash


me=$(basename "$0");
scripts/logger.sh "$me" 'info' "Called $me script"


template=$(<templates/file_preparer)

user="$(whoami)";
path="$(pwd)";

if [[ -f "/etc/systemd/system/file_preparer.service" ]]; then
        scripts/logger.sh "$me" 'debug' "file_preparer.service already exists: restarting daemon"
	sudo systemctl daemon-reload
        sudo systemctl restart "file_preparer.service"
        exit 1;
fi

sudo mkdir -p /etc/systemd/system/

echo "${template//\$\{path\}/$path}" | \
sed "s/\$user/$user/g" | sudo tee "/etc/systemd/system/file_preparer.service" > /dev/null

scripts/logger.sh "$me" 'debug' "file_preparer.service was created: starting daemon"
sudo systemctl daemon-reload
sudo systemctl enable "file_preparer.service"
sudo systemctl start "file_preparer.service"
