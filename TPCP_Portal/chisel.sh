#!/bin/bash

id=1
#echo "Hello Chisel"

sudo docker run -dv /tmp/uploads/"$id"/candidates/:/candidates/ --name job-$id grammatech/tpcp-dev && sudo docker exec -it job-$id 'echo hello'
#sleep 5
#sudo docker exec -it job-$id 'echo hello'