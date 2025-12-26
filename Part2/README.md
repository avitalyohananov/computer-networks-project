# Computer Networks Project - Part 2
For the second part of the project, we created a chat application using Python and TCP Sockets.
The system uses a central server to manage connections between clients. Users can register, connect to another user, and send private messages.

## Files
* **`server.py`** - The server code. It listens on port 5000 and handles multiple clients using threads.
* **`client.py`** - The client side. It connects to the server, asks for a username, and lets the user send commands.

## How to run
1. Open a terminal and start the server:
   python server.py

2. Open new terminals for the clients (as many as you want) and run:
   python client.py
   (Enter a username when prompted)

## Protocol & Commands
After entering your username, you can use these commands:

* "CONNECT username":
  Start a chat session with another connected user.
  Example: CONNECT alice

* "MSG text":
  Send a message to the user you are currently connected to.
  Example: MSG Hello there!

* "DISCONNECT":
  End the current chat session (but stay connected to the server).

* "exit":
  Close the application.
