#! /bin/bash

docker_env=$1

if [ ! -f  "docker-compose.yml" ]; then
  echo "docker-compose does not exist";
  touch docker-compose.yml;
fi

if [ $docker_env == "prod" ]; then
  echo "switching to prod"
  export BUILD_ENV=$(docker_env)
  sudo cp docker-compose-prod.yml docker-compose.yml
fi

if [ $docker_env == "dev" ]; then
  echo "switching to dev"
  export BUILD_ENV=$(docker_env)
  sudo cp docker-compose-dev.yml docker-compose.yml
fi