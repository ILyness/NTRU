import socket
import os
import sys
import time

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from ntru import NTRU
from ntru_pipeline import encryptMessage, qnaryBlockToCoeffs
from polymod import ConvolutionPoly
from terminal_utils import Loader, Colors, slow_print, prettify_polynomial

N, p, q, d = 17, 3, 101, 5
ntruencrypt = NTRU(N, p, q, d)

SERVER_IP = "10.133.14.133"
PORT = 65432
WAIT_TIME = 1

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_IP, PORT))

while True:
    client_name = Colors.BOB + input("What is your name? ") + Colors.RESET
    client.sendall(client_name.encode('utf-8'))
    host_name = client.recv(128).decode('utf-8')
    slow_print(f"\nHi, {client_name}! You are trying to talk with {host_name}, but {Colors.EVE}Eve{Colors.RESET} is listening.")

    slow_print(f"We will use {Colors.BOLD}NTRUEncrypt{Colors.RESET} with 𝑁 = {N}, 𝑝 = {p}, 𝑞 = {q}, 𝑑 = {d} to encrypt your message.")
    slow_print(f"Before we can send your message, we need to get {host_name}'s public key.")
    slow_print(f"Waiting for {host_name}'s public key...", end='\r', final_delay=0)
    with Loader(desc=f"Waiting for {host_name}'s public key...", end=f"{host_name} sent you the following message:"):
        h_str = client.recv(128).decode('utf-8')
    slow_print(f"\n{Colors.MESSAGE}{repr(h_str)[1:-1]}{Colors.RESET}\n")
    slow_print("We need to retrieve the original public key from the message. The key is:")
    h = ConvolutionPoly(rank=N, modulus=q, coeffs=qnaryBlockToCoeffs(h_str)) 
    slow_print(f"\n{Colors.BOLD}h{Colors.RESET} = {prettify_polynomial(h.__str__())}\n", delay=0.02)
    slow_print(f"Now that we have {host_name}'s public key, we can send them messages.")
    slow_print("Enter a message to send: ", end='')
    plaintext = input()

    ciphertext, m, r, e = encryptMessage(plaintext, N, p, q, d, h_str)
    slow_print("We need to represent your message as a polynomial. That polynomial is: ")
    slow_print(f"\n{Colors.BOLD}m{Colors.RESET} = {prettify_polynomial(m.__str__())}\n", delay=0.02)
    slow_print("We now generate a random polynomial r:")
    slow_print(f"\n{Colors.BOLD}r{Colors.RESET} = {prettify_polynomial(r.__str__())}\n", delay=0.02)
    slow_print("We now can generate your final polynomial e:")
    slow_print(f"\n{Colors.BOLD}e{Colors.RESET} = {prettify_polynomial(e.__str__())}\n", delay=0.02)
    slow_print("Like before, we now express e as your final ciphertext.")
    slow_print(f"{Colors.BOLD}Ciphertext{Colors.RESET}: {Colors.MESSAGE}{repr(ciphertext)[1:-1]}{Colors.RESET}", delay=0.02)
    slow_print(f"{Colors.EVE}Eve{Colors.RESET} can see {host_name}'s public key and your ciphertext, but she won't be able to retrieve m.")
    slow_print(f"Sending {host_name} your ciphertext.")
    client.sendall(ciphertext.encode('utf-8'))

    client.recv(128)
    print("\033[H\033[J", end="")