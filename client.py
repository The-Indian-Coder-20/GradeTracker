import socket
import threading
import tkinter as tk
from tkinter import font, simpledialog, messagebox
import random
import string

class ChatClient:
    def __init__(self, HOST="172.17.4.254", PORT=8080):
        self.HOST = HOST
        self.PORT = PORT
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.font_size = 12
        self.font_family = "Helvetica"
        self.widgets = []

        self.bg_color = "#ffffff"
        self.fg_color = "#000000"

        self.emoticon_dict = {
            ":)": "😊",
            ":(": "☹️",
            ":D": "😄",
            ":P": "😜",
            ";)": "😉",
            ":heart:": "❤️",
            ":star:": "⭐",
            ":fire:": "🔥",
            ":poop:": "💩",
            ":thumbsup:": "👍",
            ":100:": "💯",
            ":cry:": "😢",
            ":smile:": "😄",
            ":laugh:": "😂",
            ":angry:": "😠",
            ":cool:": "😎"
        }

        self.show_main_menu()

    def exit_application(self):
        self.root.quit()  # This will stop the Tkinter event loop and close the window
        self.root.destroy()  # Destroys the root window and releases resources
        exit()  # Ensures that the program terminates

    def show_main_menu(self):
        self.root = tk.Tk()
        self.root.title("🌀 Rogue Chat - Main Menu")
        self.root.geometry("360x320")  # Increased height to accommodate Exit button
        self.root.resizable(False, False)
        self.update_colors(self.root)

        label = tk.Label(self.root, text="Rogue Chat", font=(self.font_family, self.font_size + 6, "bold"))
        label.pack(pady=30)
        self.widgets.append(label)

        chat_btn = tk.Button(self.root, text="💬 Chat Servers", font=(self.font_family, self.font_size + 2),
                             width=20, height=2, command=self.launch_chat)
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

    def update_font_size(self, value):
        self.font_size = int(value)
        for widget in self.widgets:
            if isinstance(widget, (tk.Label, tk.Button, tk.Text, tk.Scale)):
                widget.configure(font=(self.font_family, self.font_size))

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

    def launch_chat(self):
        self.root.withdraw()

        try:
            self.client_socket.connect((self.HOST, self.PORT))
        except Exception as e:
            messagebox.showerror("Connection Error", "Could not connect to server:\n Server is either broken or online. \n Try again later!")
            self.root.deiconify()
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
                self.root.deiconify()
                return

            try:
                choice = self.client_socket.recv(1024).decode()
            except Exception as e:
                messagebox.showerror("Connection Error", f"Failed to receive response from server:\n{e}")
                self.root.deiconify()
                return

            if choice == "F":
                messagebox.showinfo("Alias Taken", "Alias is already in use. Please choose another one.")
                alias = ""
                continue
            else:
                break

        self.chat_window = tk.Toplevel()
        self.chat_window.title(f"Rogue Chat [{alias}]")
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
            self.client_socket.close()

    def display_message(self, msg):
        if hasattr(self, 'chat_display'):
            msg = self.replace_emoticons(msg)  # Replace emoticons with emojis
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
        self.client_socket.sendall("exit".encode())
        self.chat_window.destroy()
        self.__init__()

    def generate_random_alias(self):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=8))


if __name__ == "__main__":
    ChatClient()
