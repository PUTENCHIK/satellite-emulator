#!/bin/bash

SCRIPT_PATH="$(pwd)/scripts/crontab.sh"

(crontab -l 2>/dev/null; echo "*/5 * * * * $SCRIPT_PATH") | crontab -
