import socket
import threading
import tkinter as tk
from tkinter import font, simpledialog, messagebox
import random
import string
import time

class ChatClient:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.font_size = 14
        self.font_family = "Helvetica"
        self.widgets = []

        self.clients = []
        self.client_names = {}
        self.online_servers = []

        self.bg_color = "#ffffff"
        self.fg_color = "#000000"

        self.connected = False  # Track connection status

        self.emoticon_dict = {
            ":)": "😊", ":(": "☹️", ":D": "😄", ":P": "😜", ";)": "😉",
            ":heart:": "❤️", ":star:": "⭐", ":fire:": "🔥", ":poop:": "💩",
            ":thumbsup:": "👍", ":100:": "💯", ":cry:": "😢", ":smile:": "😄",
            ":laugh:": "😂", ":angry:": "😠", ":cool:": "😎"
        }

        self.show_main_menu()
        self.owner = False

    def get_local_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"

    def exit_application(self):
        self.root.quit()
        self.root.destroy()
        exit()

    def show_main_menu(self):
        self.root = tk.Tk()
        self.root.title("🌀 Rogue Chat - Main Menu")
        self.root.geometry("360x320")
        self.root.resizable(False, False)
        self.update_colors(self.root)

        # Title label is not affected by font size change
        label = tk.Label(self.root, text="Rogue Chat", font=(self.font_family, 20, "bold"))
        label.pack(pady=30)
        self.widgets.append(label)

        chat_btn = tk.Button(self.root, text="💬 Chat Servers", font=(self.font_family, self.font_size + 2),
                             width=20, height=2, command=self.show_server_list)
        chat_btn.pack(pady=10)
        self.widgets.append(chat_btn)

        settings_btn = tk.Button(self.root, text="⚙️ Settings", font=(self.font_family, self.font_size + 2),
                                 width=20, height=2, command=self.show_settings)
        settings_btn.pack(pady=10)
        self.widgets.append(settings_btn)

        exit_btn = tk.Button(self.root, text="❌ Exit", font=(self.font_family, self.font_size + 2),
                             width=20, height=2, command=self.exit_application)
        exit_btn.pack(pady=10)
        self.widgets.append(exit_btn)

        self.root.mainloop()

    def update_font_size(self, value):
        self.font_size = int(value)
        for widget in self.widgets:
            if isinstance(widget, (tk.Label, tk.Button, tk.Text, tk.Scale)):
                widget.configure(font=(self.font_family, self.font_size))

    def show_settings(self):
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("300x120")
        self.update_colors(settings_window)

        label = tk.Label(settings_window, text="Font Size:", font=(self.font_family, self.font_size))
        label.pack(pady=(10, 0))
        self.widgets.append(label)

        font_slider = tk.Scale(
            settings_window, from_=8, to=24, orient="horizontal",
            command=self.update_font_size, showvalue=True
        )
        font_slider.set(self.font_size)
        font_slider.pack()
        self.widgets.append(font_slider)

    def update_colors(self, parent):
        parent.configure(bg=self.bg_color)
        for widget in parent.winfo_children():
            self.widgets.append(widget)
            try:
                widget.configure(
                    bg=self.bg_color,
                    fg=self.fg_color,
                    insertbackground=self.fg_color,
                )
            except:
                pass

    def discover_servers(self):
        def listen():
            udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            udp_socket.bind(("", 54545))
            udp_socket.settimeout(1)

            while self.server_listening:
                try:
                    data, addr = udp_socket.recvfrom(1024)
                    info = data.decode().split("|")
                    if info[0] == "RogueServer":
                        name, ip, port = info[1], info[2], int(info[3])
                        server_entry = (name, ip, port)
                        if server_entry not in self.online_servers:
                            self.online_servers.append(server_entry)
                            print("Added:", server_entry)
                            self.update_server_list_ui()
                except socket.timeout:
                    continue
                except Exception as e:
                    print(f"UDP listen error: {e}")
                    break
            udp_socket.close()

        self.online_servers = []  # Reset list each time
        self.server_listening = True
        threading.Thread(target=listen, daemon=True).start()

    def show_server_list(self):
        self.root.withdraw()
        self.server_window = tk.Toplevel()
        self.server_window.title("Select Chat Server")
        self.server_window.geometry("400x400")
        self.update_colors(self.server_window)

        create_btn = tk.Button(self.server_window, text="➕ Create Server", font=(self.font_family, self.font_size),
                               command=self.create_server)
        create_btn.pack(pady=(10, 5))

        refresh_btn = tk.Button(self.server_window, text="🔄 Refresh", font=(self.font_family, self.font_size),
                                command=self.update_server_list_ui)
        refresh_btn.pack(pady=(0, 10))

        self.server_list_frame = tk.Frame(self.server_window)
        self.server_list_frame.pack(fill="both", expand=True)
        self.update_colors(self.server_list_frame)

        back_btn = tk.Button(self.server_window, text="Back to Main Menu", font=(self.font_family, self.font_size),
                             command=self.back_to_main_menu_from_server_list)
        back_btn.pack(pady=10)

        self.discover_servers()

    def update_server_list_ui(self):
        # Clear current UI list
        for widget in self.server_list_frame.winfo_children():
            widget.destroy()

        print(self.online_servers)

        if not self.online_servers:
            label = tk.Label(self.server_list_frame, text="No available servers",
                             font=(self.font_family, self.font_size))
            label.pack(pady=20)
        else:
            for name, host, port in self.online_servers:
                btn = tk.Button(self.server_list_frame, text=f"{name} ({host}:{port})",
                                font=(self.font_family, self.font_size),
                                command=lambda h=host, p=port: self.launch_chat(h, p))
                btn.pack(pady=5, fill="x", padx=20)

    def is_port_in_use(self, PORT, HOST):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind((HOST, PORT))
                return False
            except:
                messagebox.showinfo("Port in use", "Port is already in use, assigning next available port...")
                return True

    def create_server(self):
        PORT = simpledialog.askinteger("Port", "Enter the port you would like to use:")
        HOST = self.get_local_ip()

        while self.is_port_in_use(PORT, HOST):
            PORT += 1

        NAME = simpledialog.askstring("Server Name", "Enter the desired name for your server:")

        self.port = PORT
        self.host = HOST
        self.name = NAME

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.online_servers.append((NAME, HOST, PORT))
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"RogueServer|{NAME}|{HOST}|{PORT}")

        self.owner = True

        def start_discovery_responder(name, port):
            def broadcast_loop():
                self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                self.udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                message = f"RogueServer|{name}|{HOST}|{port}"
                while True:
                    try:
                        self.udp_socket.sendto(message.encode(), ("255.255.255.255", 54545))
                        time.sleep(2)
                    except Exception as e:
                        print(f"Discovery broadcast error: {e}")
                        break

            threading.Thread(target=broadcast_loop, daemon=True).start()

        def broadcast(client_name, data, sender_socket):
            for client in self.clients:
                if client != sender_socket:
                    try:
                        client.sendall(f"<{client_name}> {data}".encode())
                    except:
                        self.clients.remove(client)
                        del self.client_names[client]
                else:
                    try:
                        client.sendall(f"<Me> {data}".encode())
                    except:
                        self.clients.remove(client)
                        del self.client_names[client]

        def handle_client(client_socket, address):
            print(f"New connection from IP: {address}")
            client_name = None

            while True:
                try:
                    temp_name = client_socket.recv(1024).decode().strip()
                except:
                    return
                if temp_name in self.client_names.values():
                    client_socket.send("F".encode())
                else:
                    client_name = temp_name
                    client_socket.send("T".encode())
                    welcome = f"'{client_name}' has joined the chat!"
                    print(welcome)
                    for client in self.clients:
                        try:
                            client.sendall(welcome.encode())
                        except:
                            client.remove(client)
                    self.clients.append(client_socket)
                    self.client_names[client_socket] = client_name
                    print(self.client_names)
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
                print(f"\n{client_name} has disconnected...")
                if client_socket == self.clients[0]:
                    for client in self.clients:
                        try:
                            client.close()
                        except:
                            pass
                    self.online_servers.remove((NAME, HOST, PORT))
                    print("Here", self.online_servers)
                    server_socket.close()
                    self.udp_socket.close()
                    print("\nServer has shut down.")
                    self.discover_servers()
                elif client_socket in self.clients:
                    self.clients.remove(client_socket)
                    for client in self.clients:
                        try:
                            client.sendall(f"{client_name} has rage quit, apparently.".encode())
                        except:
                            self.clients.remove(client)
                    client_socket.close()
                    del self.client_names[client_socket]

        def server_thread():
            try:
                while True:
                    client_socket, address = server_socket.accept()
                    threading.Thread(target=handle_client, args=(client_socket, address), daemon=True).start()
            except Exception as e:
                print(f"Server error: {e}")
            finally:
                for client in self.clients:
                    try:
                        client.close()
                    except:
                        pass
                if (NAME, HOST, PORT) in self.online_servers:
                    self.online_servers.remove((NAME, HOST, PORT))
                print("Here", self.online_servers)
                server_socket.close()
                print("\nServer has shut down.")
                self.discover_servers()

        # Start the server thread
        threading.Thread(target=server_thread, daemon=True).start()

        start_discovery_responder(NAME, PORT)

        # Launch host's chat window immediately
        self.launch_chat(HOST, PORT)

    def back_to_main_menu_from_server_list(self):
        self.server_window.destroy()
        self.root.deiconify()

    def launch_chat(self, host, port):
        self.HOST = host
        self.PORT = port
        self.server_window.withdraw()

        try:
            self.client_socket.connect((self.HOST, self.PORT))
        except Exception as e:
            messagebox.showerror("Connection Error", f"Could not connect to server.\nServer is either broken or not online.\nTry again later!\n\nReason:\n{e}")
            self.server_window.deiconify()
            return

        while True:
            alias = simpledialog.askstring("Alias", "Enter your alias (1-15 characters):")
            if not alias:
                alias = self.generate_random_alias()
                messagebox.showinfo("Alias Generated", f"No alias provided. Using generated alias: {alias}")

            if not (1 <= len(alias) <= 15):
                messagebox.showerror("Invalid Alias", "Alias must be between 1 and 15 characters.")
                continue
            elif not alias.isalnum():
                messagebox.showerror("Invalid Alias", "Alias can only contain letters and numbers.")
                continue

            try:
                self.client_socket.sendall(alias.encode())
            except Exception as e:
                messagebox.showerror("Connection Error", f"Failed to send alias:\n{e}")
                self.server_window.deiconify()
                return

            try:
                choice = self.client_socket.recv(1024).decode()
            except Exception as e:
                messagebox.showerror("Connection Error", f"Failed to receive response from server:\n{e}")
                self.server_window.deiconify()
                return

            if choice == "F":
                messagebox.showinfo("Alias Taken", "Alias is already in use. Please choose another one.")
                alias = ""
                continue
            else:
                break

        self.connected = True  # Set connection status

        self.chat_window = tk.Toplevel()
        self.chat_window.title(f"Rogue Chat [{alias}] | IP: {self.get_local_ip()}")
        self.chat_window.geometry("600x400")
        self.chat_window.rowconfigure(0, weight=1)
        self.chat_window.rowconfigure(1, weight=0)
        self.chat_window.columnconfigure(0, weight=1)
        self.update_colors(self.chat_window)

        self.build_chat_ui(alias)

        threading.Thread(target=self.receive_messages, daemon=True).start()

    def build_chat_ui(self, alias):
        self.chat_display = tk.Text(self.chat_window, state="disabled", wrap="word")
        self.chat_display.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.widgets.append(self.chat_display)
        self.chat_display.configure(font=(self.font_family, self.font_size))

        self.input_container = tk.Frame(self.chat_window)
        self.input_container.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        self.input_container.columnconfigure(0, weight=1)
        self.input_container.columnconfigure(1, weight=0)
        self.input_container.columnconfigure(2, weight=0)
        self.update_colors(self.input_container)

        self.text_box = tk.Text(self.input_container, height=1, wrap="word")
        self.text_box.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        self.text_font = font.Font(family=self.font_family, size=self.font_size)
        self.text_box.configure(font=self.text_font)
        self.text_box.bind("<KeyRelease>", self.auto_resize)
        self.text_box.bind("<Configure>", self.auto_resize)
        self.widgets.append(self.text_box)

        self.send_button = tk.Button(
            self.input_container,
            text="Send",
            command=self.send_message,
            width=10
        )
        self.send_button.grid(row=0, column=1, sticky="n")
        self.widgets.append(self.send_button)
        self.send_button.configure(font=(self.font_family, self.font_size))

        self.emoji_button = tk.Button(
            self.input_container,
            text="😊",
            command=self.show_emoji_menu,
            width=4
        )
        self.emoji_button.grid(row=0, column=2, sticky="n")
        self.widgets.append(self.emoji_button)
        self.emoji_button.configure(font=(self.font_family, self.font_size))

        self.back_button = tk.Button(
            self.chat_window,
            text="Back to Main Menu",
            command=self.back_to_main_menu,
            width=20
        )
        self.back_button.grid(row=2, column=0, sticky="nsew", padx=5, pady=10)
        self.widgets.append(self.back_button)
        self.back_button.configure(font=(self.font_family, self.font_size))

    def auto_resize(self, event=None):
        content = self.text_box.get("1.0", "end-1c")
        width_pixels = self.text_box.winfo_width()
        char_width = self.text_font.measure("0")
        chars_per_line = max(width_pixels // char_width, 1)

        wrapped_lines = 0
        for paragraph in content.split("\n"):
            line_count = (len(paragraph) // chars_per_line) + 1
            wrapped_lines += line_count

        max_lines = 5
        wrapped_lines = min(wrapped_lines, max_lines)
        self.text_box.configure(height=wrapped_lines)

    def send_message(self):
        if not self.connected:
            self.display_message("⚠️ Cannot send: not connected to server.")
            return

        message = self.text_box.get("1.0", "end-1c").strip()
        if message:
            try:
                self.client_socket.sendall(message.encode())
            except:
                self.display_message("Failed to send message.")
            self.text_box.delete("1.0", "end")
            self.auto_resize()

    def receive_messages(self):
        try:
            while True:
                data = self.client_socket.recv(1024).decode()
                if not data:
                    break
                self.display_message(data)
        except:
            self.display_message("\n⚠️ Connection closed.")
        finally:
            self.connected = False
            self.client_socket.close()
            self.display_message("⚠️ Server has disconnected. You can return to the main menu.")
            # Enable the back button if it's disabled
            if hasattr(self, "back_button"):
                self.back_button.config(state="normal")

    def display_message(self, msg):
        if hasattr(self, 'chat_display'):
            msg = self.replace_emoticons(msg)
            self.chat_display.configure(state="normal")
            self.chat_display.insert("end", msg + "\n")
            self.chat_display.configure(state="disabled")
            self.chat_display.see("end")

    def replace_emoticons(self, text):
        for emoticon, emoji in self.emoticon_dict.items():
            text = text.replace(emoticon, emoji)
        return text

    def show_emoji_menu(self):
        menu = tk.Menu(self.chat_window, tearoff=0)
        for emoji in self.emoticon_dict.values():
            menu.add_command(label=emoji, command=lambda e=emoji: self.insert_emoji(e))
        try:
            x = self.emoji_button.winfo_rootx()
            y = self.emoji_button.winfo_rooty() + self.emoji_button.winfo_height()
            menu.tk_popup(x, y)
        finally:
            menu.grab_release()

    def insert_emoji(self, emoji):
        self.text_box.insert("insert", emoji)

    def back_to_main_menu(self):
        
        try:
            if self.connected:
                self.client_socket.sendall("exit".encode())
        except:
            pass  # Ignore if already closed
        self.chat_window.destroy()
        self.__init__()

    def generate_random_alias(self):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=8))


if __name__ == "__main__":
    ChatClient()
