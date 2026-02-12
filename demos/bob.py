import socket
import os
import sys
from itertools import batched
from ntru import NTRU
from polymod import ConvolutionPoly

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

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
    
    # ---------------------------------------------------------
    # ### <<< INSERT YOUR ENCRYPTION FUNCTION HERE >>> ###
    # Example: ciphertext = my_encrypt_func(message)
    # For now, we just pass it through:
    ciphertext = ''
    messages = []
    bits = []
    for c in message:
        bits.extend(list(map(int, list(format(ord(c), '08b')))))
    for block in batched(bits, ntruencrypt.N):
        block = list(block)
        if len(block) < ntruencrypt.N:
            block = block.extend([0] * (ntruencrypt.N - len(block)))
        ciphertext += ' '.join(ntruencrypt.encryptMessage(block).coeffs) + ' '

    # ---------------------------------------------------------

    # 3. Send data (must be encoded to bytes first)
    # If your encryption outputs a string, use .encode()
    # If your encryption outputs raw bytes, remove .encode()
    try:
        client.sendall(ciphertext.encode('utf-8'))
        print(f"Sent: {ciphertext}")
    except AttributeError:
        # Fallback if your function returned bytes already
        client.sendall(ciphertext)
        print(f"Sent: {ciphertext}")