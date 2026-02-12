import socket
import os
import sys
from itertools import batched
from polymod import ConvolutionPoly

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from ntru import NTRU

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
    data = conn.recv(1024)
    if not data:
        break
    
    # 2. Decode bytes back to string (so you can process it)
    received_message = data.decode('utf-8')
    coeffs = received_message.split()
    bits = []
    decrypted_message = ''
    for block in batched(coeffs, ntruencrypt.N):
        bits.extend(ntruencrypt.decryptMessage(ConvolutionPoly(ntruencrypt.N, ntruencrypt.q, list(block))).coeffs)
    for block in batched(bits, 8):
        decrypted_message += chr(int(''.join(block), 2))
    
    # ---------------------------------------------------------
    # ### <<< INSERT YOUR DECRYPTION FUNCTION HERE >>> ###
    # Example: decrypted_text = my_decrypt_func(received_message)
    # For now, we just pass it through:
    # ---------------------------------------------------------

    print(f"Received: {decrypted_message}") 