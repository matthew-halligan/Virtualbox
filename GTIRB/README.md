# GTIRB Environment

## Setup

Make sure you are in the GTIRB directory inside of the Virtualbox repo.

Issue the following command:

`./build.sh`


## Using the containers

To use the GTIRB container enviroment make sure you are in the GTIRB directory inside the Virtualbox repo.

Issue the following command:

`./start.sh`

You will be prompted for a password, the password is 'pwd'

To interact with GTIRB, access it by hostname. 

For example (inside container): `curl gtirb`


## Troubleshooting

### Building

If there are issues while running the build script it is likely an issue with docker credentials. 

Issue the following command: 

`newgrp docker`

Try to run the build script again, if that fails reboot the virtual machine.

### Running

Permssion erros might occur while attempting to run the containers. Try the advice given in the **building** troubleshooting section.

Sometimes, there might be an SSH error if the containers have been deleted and restored. Specifically, it is caused by a duplicate fingerprint. A duplicate fingerprint triggers SSH to fail and warn of man in the middle attack. 

To fix, run the fix_ssh script.

`./fix_ssh.sh`

## Manual Startup

Run the following commands:

1. `docker-compose up -d`

2. `ssh sshuser@172.20.0.7`

3. Enter the password 'pwd'

4. (Inside container) Check that GTIRB is connected: `curl gtirb`

5. (Inside container) To exit: `exit`


