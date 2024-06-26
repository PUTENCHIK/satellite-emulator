#!/bin/bash

SCRIPT_PATH="$(pwd)/scripts/crontab.sh"
if ! crontab -l | grep -Fq "$SCRIPT_PATH"; then
	(crontab -l 2>/dev/null; echo "*/5 * * * * $SCRIPT_PATH") | crontab -
fi

DATE_CHANGER="$(pwd)/src/update_date.py"
if ! crontab -l | grep -Fq "$DATE_CHANGER"; then
	(crontab -l 2>/dev/null; echo "59 23 * * * $DATE_CHANGER") | crontab -
fi
