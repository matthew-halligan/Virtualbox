git clone https://github.com/hckuo/Cozart.git

#install dependencies 
sudo apt install vim kmod qemu qemu-kvm

#build dockerfile
cd Cozart/docker;
docker build -f Dockerfile -t cozart-env:latest .
