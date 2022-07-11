#! /bin/bash

# Collect the directory the user started the script in to return to
# it at the end
ORIGINAL_DIR=$(pwd)
USER=mjhallig

curl=1
git=1
docker=1
java8=1
java11=1
python_three_eight=1
makegcc=1
maven=1
gradle=1
cmake=1
protobufc=1
protobuf=1
boost=1
doxygen=1
lisp=1
chisel=1
gtirb=1
jetbrains=1

#Start everything with an up to date working environment
sudo apt-get upgrade -y
sudo apt-get update -y

#install curl
if [ $curl == 1 ]; then
    sudo apt-get install curl -y
    echo "insecure" >> /home/$USER/.curlrc
fi


#install git
if [ $git == 1 ]; then
    sudo apt-get install git -y
fi


#Add Site Certs for known required connections
./${ORIGINAL_DIR}/add_site_cert.sh download.docker.com 443
./${ORIGINAL_DIR}/add_site_cert.sh apt.llvm.org 443
./${ORIGINAL_DIR}/add_site_cert.sh www.github.com 443

#Install docker
if [ $docker == 1 ]; then
    sudo apt-get update -y
    sudo apt-get remove docker docker-engine docker.io containerd runc

    sudo apt-get update -y
    sudo apt-get install -y ca-certificates curl gnupg lsb-release

    curl -fsSL --insecure https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

    sudo apt-get update -y

    sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose
    # If you need to install a specific docker version comment out the line above
    # and uncomment the lines below
    #sudo apt-get install docker-ce=<VERSION_STRING> docker-ce-cli=<VERSION_STRING> containerd.io
fi


#install java 8, 11
if [ $java8 == 1 ]; then
    sudo apt-get update -y
    sudo apt-get install -y openjdk-8-jdk
fi

if [ $java11 == 1 ]; then
    sudo apt-get update -y
    sudo apt-get install -y openjdk-11-jdk
fi


#install python 3.8
if [ $python_three_eight == 1 ]; then
    sudo apt-get update -y
    sudo apt-get -y upgrade
    sudo apt-get install -y python3-pip

    sudo apt install -y build-essential libssl-dev libffi-dev python3-dev
fi



#install make, gcc
if [ $makegcc == 1 ]; then
    sudo apt-get update -y
    sudo apt install build-essential -y
fi



#install maven
if [ $maven == 1 ]; then
    sudo apt update -y
    sudo apt install maven -y
    sudo ln /usr/bin/mvn /usr/bin/maven
fi


#install gradle
if [ $gradle == 1 ]; then
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
fi

#install cmake
if [ $cmake == 1 ]; then
    sudo apt-get install build-essential libssl-dev -y
    cd /tmp
    wget https://github.com/Kitware/CMake/releases/download/v3.20.0/cmake-3.20.0.tar.gz --no-check-certificate

    tar -zxvf cmake-3.20.0.tar.gz
    cd cmake-3.20.0

    sudo ./bootstrap

    sudo make

    sudo make install

    cd $ORIGINAL_DIR
fi

#install protobuf compiler
if [ $protobufc == 1 ]; then
    sudo apt install -y protobuf-compiler
fi


#install Protobuf
if [ $protobuf == 1 ]; then
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
    ##cd $ORIGINAL_DIR
fi



#install Boost
if [ $boost == 1 ]; then
    sudo apt-get update -y
    sudo apt-get install libboost-all-dev -y
fi



#install Doxygen
if [ $doxygen == 1 ]; then
    sudo apt-get install doxygen -y
fi


#install Lisp Interpreter
if [ $lisp ==1 ]; then
    sudo apt-get install -y clisp
fi


#install Chisel
if [ $chisel == 1 ]; then
    cd Chisel/
    sudo chmod 777 . -R
    sudo ./build.sh
    sudo chmod 766 . -R
    cd ..
fi

#install CBAT
if [ $cbat == 1 ]; then
    cd CBAT/
    sudo chmod 777 . -R
    sudo ./build.sh
    sudo chmod 766 . -R
    cd ..
fi


#install GTIRB
if [ $gtirb == 1 ]; then
    cd GTIRB
    sudo ./build.sh
    cd ..
fi


#install Jetbrains Toolbox
if [ $jetbrains == 1 ]; then
    wget --no-check-certificate https://download.jetbrains.com/toolbox/jetbrains-toolbox-1.24.11947.tar.gz -P ~/Downloads

    cd /opt
    sudo tar -xzvf ~/Downloads/jetbrains-toolbox-1.24.11947.tar.gz
    sudo mv jetbrains-toolbox-1.24.11947 jetbrains
    sudo ./jetbrains/jetbrains-toolbox
    cd $ORIGINAL_DIR
fi


