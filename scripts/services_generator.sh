#!/bin/bash


#template=$(cat services/service_template);
#path=/home/admin;
#echo "$template";
#eval "echo $template";

user="$(whoami)";
path="$(pwd)";

for receiver in files/*; do
	receiver="$(basename $receiver)";
	template="[Unit]

	Description=Template of daemon service
	After=network.target

	[Service]

	ExecStart=/usr/bin/python ${path}/publisher.py $receiver
	Environment=PYTHONUNBUFFERED=1
	Restart=on-failure
	Type=notify
	User=$user

	[Install]

	WantedBy=default.target"

	echo $template;
done
