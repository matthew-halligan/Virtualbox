import socket
import os

HOST = "172.20.0.8" #This would be the server IP based on the docker-compose.yml
PORT = 6000 #This would be the exposed port that we're communicating on
BUFFER_SIZE = 1 #In bytes (Only need 1 byte for indexes 0-255. Small buffer = fast read/writes)

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
        print(f"Data Decoded: {decoded_data}")
        print("")
        print(f"-=== Running GSA for binaries in /uploads/{decoded_data} ===-")
        print("")

        #Tell container to run the GSA with the passed index
        os.system(f"python3 server/run-gsa.py {decoded_data}")
        conn.send(data)

    conn.close()