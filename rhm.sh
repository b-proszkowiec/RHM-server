#!/bin/bash

RHM_PATH=/home/osmc/repo/RHM-server/rhm_server.py

echo "rhm.service: ## Starting ##" | systemd-cat -p info

python3 $RHM_PATH 

