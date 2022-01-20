#!/bin/bash

# install compose and login to docker
sudo curl -L "https://github.com/docker/compose/releases/download/1.27.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

sudo groupadd docker
sudo usermode -aG docerk $USER
newgrp docker # if login still does not work, reboot

# create working area
mkdir ~/workspace
mkdir ~/workspace/binaries
cd ~/workspace/binaries

# start containers
# need to add a line to insure docker-compose file is in workspace directory
docker-compose up -d
docker-compose down
ssh -o "UserKnownHostsFile=/dev/null" -o "StrictHostKeyChecking=no" sshuser@172.20.7

