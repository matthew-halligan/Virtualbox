#! /bin/bash

# Collect the directory the user started the script in to return to
# it at the end
ORIGINAL_DIR=$(pwd)
USER=mjhallig


#Start everything with an up to date working environment
sudo apt-get upgrade -y
sudo apt-get update -y

#install curl
sudo apt-get install curl -y
echo "insecure" >> /home/$USER/.curlrc

#install git
sudo apt-get install git -y

#Add Site Certs for known required connections
./${ORIGINAL_DIR}/add_site_cert.sh download.docker.com 443
./${ORIGINAL_DIR}/add_site_cert.sh apt.llvm.org 443
./${ORIGINAL_DIR}/add_site_cert.sh www.github.com 443

#Install docker
sudo apt-get update -y
sudo apt-get remove docker docker-engine docker.io containerd runc

sudo apt-get update -y
sudo apt-get install -y ca-certificates curl gnupg lsb-release

curl -fsSL --insecure https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg 

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update -y

sudo apt-get install -y docker-ce docker-ce-cli containerd.io
# If you need to install a specific docker version comment out the line above
# and uncomment the lines below
#sudo apt-get install docker-ce=<VERSION_STRING> docker-ce-cli=<VERSION_STRING> containerd.io

#install java 8, 11
sudo apt-get update -y
sudo apt-get install -y openjdk-8-jdk
sudo apt-get install -y openjdk-11-jdk

#install python 3.8
sudo apt-get update -y
sudo apt-get -y upgrade
sudo apt-get install -y python3-pip

sudo apt install -y build-essential libssl-dev libffi-dev python3-dev


#install make, gcc
sudo apt-get update -y
sudo apt install build-essential -y


#install maven
sudo apt update -y
sudo apt install maven -y
sudo ln /usr/bin/mvn /usr/bin/maven

#install gradle
sudo apt update -y
sudo apt install openjdk-11-jdk -y
VERSION=6.5.1
wget https://services.gradle.org/distributions/gradle-${VERSION}-bin.zip -P /tmp --no-check-certificate
sudo unzip -d /opt/gradle /tmp/gradle-${VERSION}-bin.zip
sudo ln -s /opt/gradle/gradle-${VERSION} /opt/gradle/latest

sudo touch /etc/profile.d/gradle.sh
sudo chmod 777 /etc/profile.d/gradle.sh
sudo echo "export GRADLE_HOME=/opt/gradle/latest" >> /etc/profile.d/gradle.sh
sudo echo "export PATH=${GRADLE_HOME}/bin:${PATH}" >> /etc/profile.d/gradle.sh
source /etc/profile.d/gradle.sh
# it is possible that GRADLE was not added to path correctly in this step but gradle_home 
# is available

#install ninja


#install cmake
sudo apt-get install build-essential libssl-dev -y
cd /tmp
wget https://github.com/Kitware/CMake/releases/download/v3.20.0/cmake-3.20.0.tar.gz --no-check-certificate

tar -zxvf cmake-3.20.0.tar.gz
cd cmake-3.20.0

sudo ./bootstrap

sudo make

sudo make install

cd $ORIGINAL_DIR

#install protobuf compiler
sudo apt install -y protobuf-compiler

#install Protobuf
sudo apt-get install libprotobuf-dev
#sudo apt-get install autoconf automake libtool curl make g++ unzip -y
#cd /tmp 
#git clone https://github.com/google/protobuf.git
#cd protobuf/
#git submodule update --init --recursive
#./autogen.sh
#./configure
#make
#make check
#sudo make install
#sudo ldconfig

#cd $ORIGINAL_DIR

#install Boost
sudo apt-get update -y
sudo apt-get install libboost-all-dev -y


#install Doxygen
sudo apt-get install doxygen -y


#install Lisp Interpreter
#sudo apt-get install -y clisp

#install Chisel
cd Chisel/
sudo ./build.sh
cd ..

#install CBAT
cd CBAT/
sudo ./build.sh
cd ..

#install gtirb 
cd GTIRB/
sudo ./build.sh
cd ..
#sudo apt-get update -y
#sudo apt-get install cmake -y

#wget --no-check-certificate -O - https://download.grammatech.com/gtirb/files/apt-repo/conf/apt.gpg.key | sudo apt-key add -
#sudo touch /etc/apt/apt.conf.d/100verify-peer.conf
#sudo chmod 777 /etc/apt/apt.conf.d/100verify-peer.conf
#echo >>/etc/apt/apt.conf.d/100verify-peer.conf "Acquire { https::Verify-Peer false }"
#sudo chmod 644 /etc/apt/apt.conf.d/100verify-peer.conf
#echo "deb [trusted=yes] https://download.grammatech.com/gtirb/files/apt-repo focal stable" | sudo tee -a /etc/apt/sources.list

#sudo apt-get update
#sudo apt-get install libgtirb gtirb-pprinter ddisasm -y

#sudo mkdir /tpcp
#cd /tpcp
#sudo mkdir gtirb
#cd gtirb
#sudo mkdir build
#cd build
#sudo git -c http.sslVerify=false clone https://github.com/GrammaTech/gtirb.git

#sudo cmake gtirb

#pip3 install gtirb



#sudo mkdir build
#cd build


#install gtirb server


#install bloaty

