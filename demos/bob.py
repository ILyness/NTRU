import socket

# Configuration
SERVER_IP = "10.133.14.133"
PORT = 65432

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_IP, PORT))
print(f"Connected to {SERVER_IP}\n")

while True:
    message = input("Enter message to send: ")
    
    # ---------------------------------------------------------
    # ### <<< INSERT YOUR ENCRYPTION FUNCTION HERE >>> ###
    # Example: ciphertext = my_encrypt_func(message)
    # For now, we just pass it through:
    ciphertext = message
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