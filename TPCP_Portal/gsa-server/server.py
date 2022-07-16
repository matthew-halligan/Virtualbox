import socket
import os

HOST = "172.20.0.8" #This would be the server IP based on the docker-compose.yml
PORT = 6000 #This would be the exposed port that we're communicating on
BUFFER_SIZE = 1024 #In bytes (Figure out what to limit to later. Small buffer = fast read/writes)

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
        print (f"Data Received: {data}"),data
        print("")

        decoded_data = data.decode("utf-8")
        strs = decoded_data.split(",")
        index = strs[0]
        binary = strs[1]
        transformedBinary = strs[2]

        print(f"Data Decoded: {index} {binary} {transformedBinary}")
        print("")
        print(f"-=== Running GSA for binaries in /uploads/{index} ===-")
        print("")

        #Tell container to run the GSA with the passed index
        os.system(f"python3 server/run_gsa.py {index} {binary} {transformedBinary}")
        conn.send(data)

    conn.close()