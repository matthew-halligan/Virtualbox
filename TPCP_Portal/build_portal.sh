#! /bin/bash


if [ $1 ]; then
    build_version=$1;
    sudo docker build -t tpcp_portal:v$(build_version) .
else
  echo "Must include a build version";
fi

