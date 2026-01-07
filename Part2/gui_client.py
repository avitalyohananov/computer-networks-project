import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox

BG_MAIN = "#2b2b2b"
BG_INPUT = "#383838"
TEXT_COLOR = "#ffffff"
BTN_BLUE = "#007acc"
BTN_RED = "#d9534f"
BTN_GREEN = "#5cb85c"

HOST = '127.0.0.1'
PORT = 5000

class ChatClient:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Python Chat")
        self.window.geometry("500x600")
        self.window.configure(bg=BG_MAIN)

        self.sock = None
        self.username = ""
        self.is_connected = False
        self.running = True

        self.setup_ui()
        self.window.mainloop()

    def setup_ui(self):        
        self.top_frame = tk.Frame(self.window, bg=BG_MAIN, pady=10)
        self.top_frame.pack(fill='x', padx=10)

        tk.Label(self.top_frame, text="Username:", bg=BG_MAIN, fg=TEXT_COLOR).pack(side='left')
        
        self.entry_user = tk.Entry(self.top_frame, bg=BG_INPUT, fg=TEXT_COLOR, insertbackground='white')
        self.entry_user.pack(side='left', padx=5)
        
        self.btn_login = tk.Button(self.top_frame, text="Login", bg=BTN_BLUE, fg="white", command=self.login)
        self.btn_login.pack(side='left', padx=5)

        self.peer_frame = tk.Frame(self.window, bg=BG_MAIN, pady=5)
        self.peer_frame.pack(fill='x', padx=10)
        
        tk.Label(self.peer_frame, text="Connect to:", bg=BG_MAIN, fg=TEXT_COLOR).pack(side='left')
        
        self.entry_target = tk.Entry(self.peer_frame, bg=BG_INPUT, fg=TEXT_COLOR, insertbackground='white')
        self.entry_target.pack(side='left', padx=5)
        
        self.btn_connect = tk.Button(self.peer_frame, text="Connect", bg=BTN_GREEN, fg="white", state='disabled', command=self.connect_to_peer)
        self.btn_connect.pack(side='left', padx=2)
        
        self.btn_disconnect = tk.Button(self.peer_frame, text="Disconnect", bg=BTN_RED, fg="white", state='disabled', command=self.disconnect_peer)
        self.btn_disconnect.pack(side='left', padx=2)

        self.chat_area = scrolledtext.ScrolledText(self.window, bg=BG_INPUT, fg=TEXT_COLOR, font=("Arial", 10))
        self.chat_area.pack(padx=10, pady=10, expand=True, fill='both')
        self.chat_area.config(state='disabled')

        self.chat_area.tag_config('me', foreground="#4da6ff")
        self.chat_area.tag_config('peer', foreground="#85e085")
        self.chat_area.tag_config('sys', foreground="yellow")
        self.chat_area.tag_config('error', foreground="#ff4d4d")

        self.bottom_frame = tk.Frame(self.window, bg=BG_MAIN, pady=10)
        self.bottom_frame.pack(fill='x', padx=10)

        self.entry_msg = tk.Entry(self.bottom_frame, bg=BG_INPUT, fg=TEXT_COLOR, font=("Arial", 11), insertbackground='white')
        self.entry_msg.pack(side='left', expand=True, fill='x', padx=5)
        self.entry_msg.bind("<Return>", lambda e: self.send_message())

        self.btn_send = tk.Button(self.bottom_frame, text="Send", bg=BTN_BLUE, fg="white", width=10, command=self.send_message)
        self.btn_send.pack(side='right')

    def login(self):
        user = self.entry_user.get()
        if not user:
            messagebox.showerror("Error", "Please enter a username")
            return
            
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((HOST, PORT))
            self.sock.send((user + "\n").encode())
            
            self.username = user
            self.btn_login.config(state='disabled', text=f"Logged as: {user}")
            self.entry_user.config(state='disabled')
            self.btn_connect.config(state='normal')
            
            threading.Thread(target=self.receive_loop, daemon=True).start()
            
        except Exception as e:
            messagebox.showerror("Connection Error", str(e))

    def connect_to_peer(self):
        target = self.entry_target.get()
        if target:
            self.sock.send(f"CONNECT {target}\n".encode())

    def disconnect_peer(self):
        self.sock.send("DISCONNECT\n".encode())

    def send_message(self):
        msg = self.entry_msg.get()
        if not msg: return
        
        if self.is_connected:
            self.sock.send(f"MSG {msg}\n".encode())
            self.add_to_chat(f"Me: {msg}", 'me')
            self.entry_msg.delete(0, 'end')
        else:
            messagebox.showwarning("Not Connected", "You are not connected to anyone.\nPlease connect to a user first.")

    def add_to_chat(self, text, tag=None):
        self.chat_area.config(state='normal')
        self.chat_area.insert('end', text + "\n", tag)
        self.chat_area.see('end')
        self.chat_area.config(state='disabled')

    def receive_loop(self):
        while self.running:
            try:
                data = self.sock.recv(1024).decode()
                if not data: break
                
                for line in data.split('\n'):
                    line = line.strip()
                    if line: self.parse_message(line)
            except:
                break
        self.window.quit()

    def parse_message(self, msg):
        if "connected to" in msg or "connected to you" in msg:
            self.is_connected = True
            self.btn_connect.config(state='disabled')
            self.btn_disconnect.config(state='normal')
            self.add_to_chat(f"--- System: {msg} ---", 'sys')
            
        elif "disconnected" in msg:
            self.is_connected = False
            self.btn_connect.config(state='normal')
            self.btn_disconnect.config(state='disabled')
            self.add_to_chat("--- System: Chat ended ---", 'sys')
            
            if "disconnected from" in msg or "disconnected" in msg:
                 messagebox.showinfo("Chat Ended", "The other user has disconnected.")
            
        elif ":" in msg and not msg.startswith("INFO") and not msg.startswith("ERROR"):
            parts = msg.split(":", 1)
            sender = parts[0]
            content = parts[1]
            self.add_to_chat(f"{sender}: {content}", 'peer')

        elif msg.startswith("ERROR:"):
            messagebox.showerror("Error", msg)
            
            if "taken" in msg:
                self.btn_login.config(state='normal', text="Login")
                self.entry_user.config(state='normal')
                self.btn_connect.config(state='disabled')
                self.username = ""
            
            self.add_to_chat(msg, 'error')
            
        else:
            self.add_to_chat(msg)

if __name__ == "__main__":
    ChatClient()
