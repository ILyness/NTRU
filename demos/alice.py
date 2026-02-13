import socket
import os
import sys
from itertools import batched
from polymod import ConvolutionPoly

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from ntru import NTRU
from ntru_pipeline import decryptMessage

ntruencrypt = NTRU(13, 3, 101, 5)
f_coeffs = [-1, 1, 0, -1, 1, -1, 1, 1, 1, -1, 1, 0, -1]
g_coeffs = [1, 1, 1, 0, 0, -1, -1, 0, -1, 1, 1, -1, -1]
ntruencrypt.createKeys(f_coeffs, g_coeffs)

# Configuration
HOST = '0.0.0.0'  # Listen on all network interfaces
PORT = 65432      # Port to listen on

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

conn, addr = server.accept()

while True:
    # 1. Receive the raw bytes from the network
    data = conn.recv(4096)
    if not data:
        break
    
    # 2. Decode bytes back to string (so you can process it)
    ciphertext = data.decode('utf-8')
    print(f"Received ciphertext: {ciphertext}") 
    plaintext = decryptMessage(ciphertext, ntruencrypt)
    print(f"Recovered plaintext: {plaintext}") 