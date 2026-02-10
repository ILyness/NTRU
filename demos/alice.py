import socket

# Configuration
HOST = '0.0.0.0'  # Listen on all network interfaces
PORT = 65432      # Port to listen on

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print(f"Listening for connections on port {PORT}...")
conn, addr = server.accept()
print(f"Connected by {addr}\n")

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