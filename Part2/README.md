# Computer Networks Project

This project is a simple chat application implemented in Python using TCP sockets.

## Files
- server.py - Server implementation that handles multiple clients and one to one chat.
- client.py - Client implementation for sending and receiving messages.

## How to run
1. Start the server:
   python server.py

2. Open two or more terminals and run the client:
   python client.py

## Protocol
- After connecting to the server, the client sends a username.
- Supported commands:
  - CONNECT <username>
  - MSG <text>
  - DISCONNECT
