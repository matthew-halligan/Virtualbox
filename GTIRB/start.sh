#!/bin/bash
docker-compose up -d
ssh sshuser@172.20.0.7
docker-compose down
ssh -o "UserKnownHostsFile=/dev/null" -o "StrictHostKeyChecking=no" sshuser@172.20.0.7
