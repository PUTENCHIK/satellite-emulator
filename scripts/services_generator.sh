#!/bin/bash

template=$(<services/service_template)

user="$(whoami)";
path="$(pwd)";

for dir in files/*/; do
    receiver=$(basename "$dir")

    if [[ -f "/etc/systemd/system/$receiver.service" ]]; then
        continue
    fi

    rnx_file=$(find "$dir" -name '*.rnx' | sort)
    rnx_file=${rnx_file[0]}
    
    if [[ -n $rnx_file ]]; then
        date=$(basename "$rnx_file")
        
        sudo mkdir -p /etc/systemd/system/
        
        echo "${template//\$\{path\}/$path}" | \
        sed "s/\$receiver/$receiver/g" | \
        sed "s/\$date/$date/g" | \
        sed "s/\$user/$user/g" | sudo tee "/etc/systemd/system/$receiver.service" > /dev/null
        
        sudo systemctl daemon-reload
        sudo systemctl enable "$receiver.service"
    fi
done
