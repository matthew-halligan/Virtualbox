#!/bin/bash
docker-compose up -d && sleep 5
ssh sshuser@172.20.0.7 
docker-compose down 

