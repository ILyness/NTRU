import socket
import os
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from ntru import NTRU

ntruencrypt = NTRU()
f_coeffs = [-1, 0, 1, 1, -1, 0, 1]
g_coeffs = [0, -1, -1, 0, 1, 0, 1]
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
    
    # ---------------------------------------------------------
    # ### <<< INSERT YOUR DECRYPTION FUNCTION HERE >>> ###
    # Example: decrypted_text = my_decrypt_func(received_message)
    # For now, we just pass it through:
    final_output = received_message 
    # ---------------------------------------------------------

    print(f"Received: {final_output}") 