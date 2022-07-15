import socket
import sys

HOST = "172.20.0.8"  # The gsa container's hostname or IP address
PORT = 6000  # The port used by the server GSA container
BUFFER_SIZE = 1 #One byte needed for indexes 0-255

#This would be the index inside the uploads folder
i = int(sys.argv[1])
index_encoded = str(i).encode()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(index_encoded)
    data = s.recv(BUFFER_SIZE)

print(f"Successfully sent index: {data!r}")
print(f"Metrics for analysis are found in /uploads/{i}")