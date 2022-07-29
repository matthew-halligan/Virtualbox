import socket
import os
import sys

import global_items as gi

HOST = gi.IP_HOST_GSA #This would be the server IP based on the docker-compose-dev.yml
PORT = gi.PORT_HOST_GSA #This would be the exposed port that we're communicating on
BUFFER_SIZE = 1024#In bytes (Only need 1 byte for indexes 0-255. Small buffer = fast read/writes)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(1)

while True:    
    conn, addr = s.accept()

    print(f'Connection address: {addr}')
    print("")

    while True:
        data = conn.recv(BUFFER_SIZE)
        if not data: break
        print(f"Data Received: {data}"), data
        print("")

        decoded_data = data.decode("utf-8")
        strs = decoded_data.split(",")
        index = strs[0]
        binary = strs[1]
        transformed_binary = strs[2]
        metrics_collection = strs[3]

        print(f"Data Decoded: {index} {binary} {transformed_binary} {metrics_collection}")
        print("")
        print(f"-=== Running GSA for binaries in /uploads/{index} ===-")
        print("")

        #Tell container to run the GSA with the passed index
        os.system(f"python3 server/run_gsa.py {index} {binary} {transformed_binary} {metrics_collection}")
        conn.send(data)

    conn.close()