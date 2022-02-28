FROM ubuntu:20.04

WORKDIR /home/sshuser/binaries
RUN apt-get update
RUN apt-get install -y openssh-server
RUN apt-get install -y python3-pip
RUN apt-get install -y git
RUN git config --global user.email "gtirb@gtirb.net"
RUN git config --global user.name "GTIRB" 
RUN pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org angr
RUN python3 -m pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org ROPgadget
RUN git clone -c http.sslVerify=false https://github.com/michaelbrownuc/GadgetSetAnalyzer.git
RUN apt-get install -y curl
RUN groupadd sshgroup && useradd -ms /bin/bash -g sshgroup sshuser
RUN echo 'sshuser:pwd' | chpasswd
EXPOSE 22
ENTRYPOINT service ssh start & bash 

