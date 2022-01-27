#!/bin/bash

# install compose and login to docker
sudo curl -k -L "https://github.com/docker/compose/releases/download/1.27.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# uncomment if recieving login errors 
sudo groupadd docker || true
sudo usermod -aG docker $USER || true
# newgrp docker || true 

docker login

# create working area

mkdir ~/workspace
mkdir ~/workspace/binaries
cp ./docker-compose.yml ~/workspace
cd ~/workspace


# start containers
# need to add a line to insure docker-compose file is in workspace directory
docker-compose up -d
docker-compose down

