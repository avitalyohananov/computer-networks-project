# Computer Networks Project - Part 2
For the second part of the project, we created a chat application using Python and TCP Sockets.
The system includes a server that manages the connections and clients that can send messages to each other.

## Files
* **`server.py`** - The server code. It handles multiple clients using threads.
* **`client.py`** - The client side. It connects to the server and handles user input.

## How to run
1. Open a terminal and run the server:
   ```bash
   python server.py
   ```

2. Open new terminals for the clients and run:
   ```bash
   python client.py
   ```

## Protocol
We used a simple text protocol with these commands:
* `CONNECT <name>` - Register a username.
* `GET_USERS` - Get a list of online users.
* `MSG <name> <message>` - Send a private message.
* `DISCONNECT` - Close the connection.
