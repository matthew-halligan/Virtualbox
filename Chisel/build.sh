#! /bin/sh
sudo docker build -t chisel .
docker run --privileged -it chisel

#run chisel with test scripts 
chisel --build ./test.sh -- make

#HTML visualize 
chisel --xref ./test.sh file.c
