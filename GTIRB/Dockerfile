FROM ubuntu:20.04

WORKDIR /home/sshuser/binaries
RUN apt-get update
RUN apt-get install -y openssh-server
RUN apt-get install -y python3-pip
RUN python3 -m pip install --user virtualenv
RUN pip install angr
RUN python3 -m pip install ROPgadget
RUN apt-get install -y curl
RUN groupadd sshgroup && useradd -ms /bin/bash -g sshgroup sshuser
RUN echo 'sshuser:pwd' | chpasswd
EXPOSE 22
ENTRYPOINT service ssh start & bash 

