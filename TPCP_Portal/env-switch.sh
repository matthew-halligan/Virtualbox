#! /bin/bash

docker_env=$1
echo $docker_env
echo "prod"
if [ ! -f  "docker-compose.yml" ]; then
  echo "docker-compose does not exist";
  touch docker-compose.yml;
fi

if [ $docker_env == "prod" ]; then
  echo "switching to prod"
  sudo cp docker-compose-prod.yml docker-compose.yml
fi

if [ $docker_env == "dev" ]; then
  echo "switching to dev"
  sudo cp docker-compose-dev.yml docker-compose.yml
fi