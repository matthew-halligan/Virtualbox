#! /bin/sh
sudo docker build -t chisel .
docker run --privileged -it chisel
