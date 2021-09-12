#!/bin/bash

PATH=/home/pi/repo/RHM-server/rhm-server.py

echo "rhm.service: ## Starting ##" | systemd-cat -p info

python3 $PATH 

