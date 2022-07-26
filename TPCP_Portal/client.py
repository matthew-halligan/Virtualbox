import socket
import sys
import global_items as gi

HOST = gi.IP_HOST_GSA  # The gsa container's hostname or IP address
PORT = gi.PORT_HOST_GSA  # The port used by the server GSA container
BUFFER_SIZE = 1024 #Figure out limit later. Smaller buffer = faster writes

# TODO: Call this function from app.upload_file() after upload/download completion
def send_data_to_GSA_server(index, sourceBinaryName, transformBinaryName):
    data_encoded = str(index + "," + sourceBinaryName + ',' + transformBinaryName).encode()
    print(data_encoded)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(data_encoded)
        data = s.recv(BUFFER_SIZE)
     
    print(f"Successfully sent {data!r} to GSA server", flush=True)
    print(f"Metrics for analysis are found in /uploads/{index}", flush=True)
