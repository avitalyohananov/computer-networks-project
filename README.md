# Computer Networks project

This project implements a simple chat system using TCP sockets in Python.

## Files
- server.py – Server side implementation (multi-client, one-to-one chat)
- client.py – Client side implementation

## How to run
1. Run the server:
   python server.py

2. Run two or more clients in separate terminals:
   python client.py

## Protocol
- After connecting, the client sends a username (one line).
- Commands:
  - CONNECT <username>
  - MSG <text>
  - DISCONNECT
