print("Client started")

import socket
import threading
import sys

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5000  

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_socket.connect((SERVER_IP, SERVER_PORT))
except ConnectionRefusedError:
    print("Error: Could not connect to server. Is it running?")
    sys.exit()


username = input("Enter Username: ")
client_socket.send((username + "\n").encode()) 

def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                print("\nServer disconnected")
                client_socket.close()
                break 
            print("\n" + message.strip())
        except:
            print("Error receiving message")
            break

receive_thread = threading.Thread(target=receive_messages, daemon=True)
receive_thread.start()

print("Commands: CONNECT <user>, MSG <text>, DISCONNECT")

while True:
    try:
        message = input()
        if message.lower() == "exit":
            client_socket.close()
            break
        client_socket.send((message + "\n").encode())
        
    except OSError:
        break
