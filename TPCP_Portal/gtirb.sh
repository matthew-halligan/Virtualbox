#! /bin/sh

echo "Hello World"

transforms=$1
executable=$2
DOCKER_HOSTNAME="gtirb"


curl -F transform=${transforms} -F binary=@${executable}.exe --output ${executable}.gtirb $DOCKER_HOSTNAME
