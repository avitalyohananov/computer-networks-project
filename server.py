import socket
import threading

HOST = "127.0.0.1"
PORT = 5000

users = {}
peers = {}
lock = threading.Lock()

def send_to_user(username, text):
    with lock:
        entry = users.get(username)
    if not entry:
        return
    _, out_file = entry
    try:
        out_file.write(text + "\n")
        out_file.flush()
    except:
        pass

def disconnect_pair(username):
    with lock:
        other = peers.pop(username, None)
        if other is not None and peers.get(other) == username:
            peers.pop(other, None)

    if other:
        send_to_user(other, f"INFO: {username} disconnected")
        send_to_user(username, f"INFO: disconnected from {other}")
    else:
        send_to_user(username, "INFO: not connected")


def handle_client(client_socket, client_address):
    print("Client connected:", client_address)

    client_file = client_socket.makefile("r", encoding="utf-8", newline="\n")
    client_out  = client_socket.makefile("w", encoding="utf-8", newline="\n")

    username = client_file.readline().strip()
    if not username:
        client_out.write("ERROR: empty username\n")
        client_out.flush()
        client_socket.close()
        return

    with lock:
        if username in users:
            client_out.write("ERROR: username already taken\n")
            client_out.flush()
            client_socket.close()
            return
        users[username] = (client_socket, client_out)
        peers[username] = None

    client_out.write("INFO: registered\n")
    client_out.flush()
    print(f"User registered: {username}")

    while True:
        line = client_file.readline()
        if not line:
            print(f"Client disconnected: {username}")
            break

        line = line.strip()

        if line.startswith("CONNECT "):
            target = line.split(" ", 1)[1].strip()

            if target == username:
                client_out.write("ERROR: cannot connect to yourself\n")
                client_out.flush()
                continue

            with lock:
                target_exists = target in users
                my_peer = peers.get(username)
                target_peer = peers.get(target)

            if not target_exists:
                client_out.write("ERROR: user not found\n")
                client_out.flush()
                continue

            if my_peer is not None:
                client_out.write("ERROR: already connected. DISCONNECT first\n")
                client_out.flush()
                continue

            if target_peer is not None:
                client_out.write("ERROR: target is already connected\n")
                client_out.flush()
                continue

            with lock:
                peers[username] = target
                peers[target] = username

            client_out.write(f"INFO: connected to {target}\n")
            client_out.flush()
            send_to_user(target, f"INFO: {username} connected to you")
            continue

        if line == "DISCONNECT":
            disconnect_pair(username)
            continue

        if line.startswith("MSG "):
            text = line.split(" ", 1)[1]

            with lock:
                other = peers.get(username)

            if other is None:
                client_out.write("ERROR: not connected. Use CONNECT <name>\n")
                client_out.flush()
                continue

            send_to_user(other, f"{username}: {text}")
            client_out.write("INFO: sent\n")
            client_out.flush()
            continue

        client_out.write("ERROR: unknown command. Use CONNECT/MSG/DISCONNECT\n")
        client_out.flush()

    disconnect_pair(username)

    with lock:
        users.pop(username, None)
        peers.pop(username, None)

    try:
        client_file.close()
        client_out.close()
    except:
        pass
    client_socket.close()


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()
print("Server is running... waiting for clients")

while True:
    client_socket, client_address = server_socket.accept()
    threading.Thread(
        target=handle_client,
        args=(client_socket, client_address),
        daemon=True
    ).start()
