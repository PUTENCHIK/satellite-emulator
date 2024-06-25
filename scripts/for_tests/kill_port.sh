#!/bin/bash


sudo lsof -t -i tcp:$1 | xargs kill -9
