#!/bin/bash


me=$(basename "$0");
scripts/logger.sh "$me" 'info' "Called $me script to kill port $1"

sudo lsof -t -i tcp:$1 | xargs kill -9
