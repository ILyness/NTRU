import socket
import os
import sys
import time

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from ntru import NTRU
from ntru_pipeline import decryptMessage, qnaryCoeffsToBlock, slow_print

N, p, q, d = 17, 3, 101, 5
ntruencrypt = NTRU(N, p, q, d)

HOST = '0.0.0.0'  
PORT = 65432  
WAIT_TIME = 1    

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

conn, addr = server.accept()

while True:
    host_name = input("What is your name? ")
    slow_print(f"Hi, {host_name}!")
    conn.sendall(host_name.encode('utf-8'))
    client_name = conn.recv(128).decode('utf-8')
    slow_print(f"{client_name} would like to talk with you, but Eve is listening.")
    time.sleep(WAIT_TIME)
    slow_print(f"We will use NTRUEncrypt with N={N}, p={p}, q={q}, d={d} to encrypt {client_name}'s message.")
    time.sleep(WAIT_TIME)
    slow_print("Here are your generated private keys:")
    h_coeffs = ntruencrypt.createRandomKeys()
    slow_print(f"f =  {ntruencrypt.f}")
    slow_print(f"g =  {ntruencrypt.g}")
    time.sleep(WAIT_TIME)
    slow_print("The resulting public key is:")
    slow_print(f"h = {ntruencrypt.h}")
    time.sleep(WAIT_TIME)
    h_str = qnaryCoeffsToBlock(ntruencrypt.h.coeffs, q)
    slow_print("We need to turn your public key into a message we can send. This message is:")
    
    slow_print(repr(h_str)[1:-1])
    time.sleep(WAIT_TIME)
    slow_print(f"Sending {client_name} your public key.")
    conn.sendall(h_str.encode('utf-8'))

    data = conn.recv(4096)
    if not data:
        break

    ciphertext = data.decode('utf-8')
    slow_print(f"{client_name} has sent you the following ciphertext:")
    slow_print(repr(ciphertext)[1:-1])
    time.sleep(WAIT_TIME)
    slow_print("We can use your private keys to decrypt the message. The decrypted result is:")
    plaintext = decryptMessage(ciphertext, ntruencrypt)
    slow_print(plaintext)

    time.sleep(5)
    print("\033[H\033[J", end="")