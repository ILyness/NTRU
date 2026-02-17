import socket
import os
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from ntru import NTRU
from ntru_pipeline import decryptMessage, qnaryCoeffsToBlock

ntruencrypt = NTRU(13, 3, 101, 5)
f_coeffs = [-1, 1, 0, -1, 1, -1, 1, 1, 1, -1, 1, 0, -1]
g_coeffs = [1, 1, 1, 0, 0, -1, -1, 0, -1, 1, 1, -1, -1]
ntruencrypt.createKeys(f_coeffs, g_coeffs)

HOST = '0.0.0.0'  
PORT = 65432      

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

conn, addr = server.accept()
conn.sendall(qnaryCoeffsToBlock(ntruencrypt.h))

while True:
    data = conn.recv(4096)
    if not data:
        break

    ciphertext = data.decode('utf-8')
    print(f"Received ciphertext: {ciphertext}") 
    plaintext = decryptMessage(ciphertext, ntruencrypt)
    print(f"Recovered plaintext: {plaintext}") 