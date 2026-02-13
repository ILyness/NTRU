import socket
import os
import sys
from itertools import batched
from polymod import ConvolutionPoly

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from ntru import NTRU
from ntru_pipeline import encryptMessage

ntruencrypt = NTRU(13, 3, 101, 5)
f_coeffs = [-1, 1, 0, -1, 1, -1, 1, 1, 1, -1, 1, 0, -1]
g_coeffs = [1, 1, 1, 0, 0, -1, -1, 0, -1, 1, 1, -1, -1]
ntruencrypt.createKeys(f_coeffs, g_coeffs)

# Configuration
SERVER_IP = "10.133.14.133"
PORT = 65432

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_IP, PORT))

while True:
    message = input("Enter message to send: ")
    ciphertext = encryptMessage(message, ntruencrypt)

    try:
        client.sendall(ciphertext.encode('utf-8'))
    except AttributeError:
        client.sendall(ciphertext)
    print(f"Sent: {ciphertext}")