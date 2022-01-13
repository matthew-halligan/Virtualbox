#! /bin/sh

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


#install java 8, 11
sudo apt-get update -y
sudo apt-get install -y openjdk-8-jdk
sudo apt-get install -y openjdk-11-jdk


#install python 3.8
sudo apt-get update -y
sudo apt-get -y upgrade
sudo apt-get install -y python3-pip

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


wget --no-check-certificate https://osate-build.sei.cmu.edu/download/osate/stable/2.7.1-vfinal/products/osate2-2.7.1-vfinal-linux.gtk.x86_64.tar.gz -P ~/Downloads/

mkdir /opt/Osate
cd /opt/Osate

tar -xvf ~/Downloads/osate2-2.7.1-vfinal-linux.gtk.x86_64.tar.gz

sudo ln -s /opt/Osate/osate /bin/osate
