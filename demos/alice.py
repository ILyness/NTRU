import socket
import os
import sys
import time

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from ntru import NTRU
from ntru_pipeline import decryptMessage, qnaryCoeffsToBlock
from terminal_utils import Loader, Colors, slow_print, prettify_polynomial
from constants import *

N, p, q, d = 17, 3, 101, 5
ntruencrypt = NTRU(N, p, q, d)

HOST = '0.0.0.0'  
WAIT_TIME = 1    

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

conn, addr = server.accept()


while True:
    conn.sendall("done".encode('utf-8'))
    print("\033[H\033[J", end="")

    host_name = Colors.ALICE + input("What is your name? ") + Colors.RESET
    slow_print(f"\nHi, {host_name}!")
    conn.sendall(host_name.encode('utf-8'))
    client_name = conn.recv(128).decode('utf-8')
    slow_print(f"{client_name} would like to talk with you, but {Colors.EVE}Eve{Colors.RESET} is listening.")
    slow_print(f"We will use {Colors.BOLD}NTRUEncrypt{Colors.RESET} with 𝑁 = {N}, 𝑝 = {p}, 𝑞 = {q}, 𝑑 = {d} to encrypt {client_name}'s message.")
    slow_print(f"Before {client_name} can send you a message, we need to give them your public key.")
    slow_print("Here are your generated private keys:")
    h_coeffs = ntruencrypt.createRandomKeys()
    slow_print(f"\n{Colors.BOLD}f{Colors.RESET} =  {prettify_polynomial(ntruencrypt.f.__str__())}\n", delay=0.01)
    slow_print(f"\n{Colors.BOLD}g{Colors.RESET} =  {prettify_polynomial(ntruencrypt.g.__str__())}\n", delay=0.01)
    slow_print("The resulting public key is:")
    slow_print(f"\n{Colors.BOLD}h{Colors.RESET} = {prettify_polynomial(ntruencrypt.h.__str__())}\n", delay=0.01)
    h_str = qnaryCoeffsToBlock(ntruencrypt.h.coeffs, q)
    slow_print("We need to turn your public key into a message we can send. This message is:")
    slow_print(f"\n{Colors.MESSAGE}{h_str}{Colors.RESET}\n")
    slow_print(f"Sending {client_name} your public key.")
    conn.sendall(h_str.encode('utf-8'))

    slow_print(f"Waiting for {client_name}'s message...", end='\r', final_delay=0)
    with Loader(desc=f"Waiting for {client_name}'s message...", end=f"{client_name} has sent you their ciphertext."):
        data = conn.recv(4096)
    ciphertext = data.decode('utf-8')
    slow_print(f"\n{Colors.BOLD}Ciphertext{Colors.RESET}: {Colors.MESSAGE}{ciphertext}{Colors.RESET}\n", delay=0.01)
    slow_print(f"{Colors.EVE}Eve{Colors.RESET} can see your public key and {client_name}'s ciphertext, but she won't be able to retrieve m.")
    slow_print("However, you can use your private keys to decrypt the message. The decrypted result is:")
    plaintext = decryptMessage(ciphertext, ntruencrypt)
    slow_print(plaintext)

    time.sleep(5)