sudo apt-get update -y
sudo apt-get install cmake -y

wget --no-check-certificate -O - https://download.grammatech.com/gtirb/files/apt-repo/conf/apt.gpg.key | sudo apt-key add -

sudo touch /etc/apt/apt.conf.d/100verify-peer.conf
sudo chmod 777 /etc/apt/apt.conf.d/100verify-peer.conf
echo >>/etc/apt/apt.conf.d/100verify-peer.conf "Acquire { https::Verify-Peer false }"
sudo chmod 644 /etc/apt/apt.conf.d/100verify-peer.conf
echo "deb [trusted=yes] https://download.grammatech.com/gtirb/files/apt-repo focal stable" | sudo tee -a /etc/apt/sources.list

sudo apt-get update
sudo apt-get install libgtirb gtirb-pprinter ddisasm -y

sudo mkdir /tpcp
cd /tpcp
sudo mkdir gtirb
cd gtirb
sudo mkdir build
cd build

sudo git clone https://github.com/GrammaTech/gtirb.git

sudo cmake gtirb

pip3 install gtirb

sudo mkdir build
cd build
