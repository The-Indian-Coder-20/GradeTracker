"""
import socket, threading

clients = []
client_names = {}

def broadcast(client_name, data, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.sendall(f"<{client_name}> {data}".encode())
            except:
                client.remove(client)
        else:
            try:
                client.sendall(f"<Me> {data}".encode())
            except:
                client.remove(client)


def handle_client(client_socket, address):
    print(f"New connection from IP: {address}")
    client_name = None

    while True:
        try:
            temp_name = client_socket.recv(1024).decode().strip()
        except:
            return
        if temp_name in client_names.values():
            client_socket.send("F".encode())
        else:
            client_name = temp_name
            client_socket.send("T".encode())
            welcome = f"'{client_name}' has joined the chat!"
            print(welcome)
            for client in clients:
                try:
                    client.sendall(welcome.encode())
                except:
                    client.remove(client)
            clients.append(client_socket)
            client_names[client_socket] = client_name
            print(client_names)
            break

    try:
        while True:
            data = client_socket.recv(1024).decode()
            if data.lower() == "exit":
                break
            broadcast(client_name, data, client_socket)
    except:
        pass
    finally:
        print(f"{client_name} has disconnected...")
        clients.remove(client_socket)
        for client in clients:
            try:
                client.sendall(f"{client_name} has rage quit, apparently.".encode())
            except:
                client.remove(client)
        client_socket.close()
        del client_names[client_socket]

def start_server(HOST = "172.17.4.254", PORT = 8080):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Server is running on {HOST}:{PORT}")

    try:
        while True:
            client_socket, address = server_socket.accept()
            threading.Thread(target = handle_client, args = (client_socket, address), daemon = True).start()
    except KeyboardInterrupt:
        print("\n Server is shutting down...")
    finally:
        for client in clients:
            client.close()
        server_socket.close()
        print("\n Server has shut down.")

if __name__ == '__main__':
    start_server()
"""

import socket
import threading

def server_discovery_listener(PORT=1025, DISCOVERY_PORT=1025):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("", DISCOVERY_PORT))  # Listening for discovery requests

    print(f"Server discovery listener started on port {DISCOVERY_PORT}")

    while True:
        try:
            # Listen for a discovery request (broadcast)
            message, addr = server_socket.recvfrom(1024)

            if message.decode() == "DISCOVER_SERVER":
                # Respond with server details
                server_info = f"{socket.gethostbyname(socket.gethostname())}:{PORT}"
                server_socket.sendto(server_info.encode(), addr)
                print(f"Sent server info {server_info} to {addr}")
        except Exception as e:
            print(f"Error during server discovery: {e}")

# Start the server discovery listener in a thread
threading.Thread(target=server_discovery_listener, daemon=True).start()
