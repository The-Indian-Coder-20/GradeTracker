import tkinter as tk

class UsernamePopup(tk.Toplevel):
    def __init__(self, parent, on_submit):
        super().__init__(parent)
        self.title("Enter Username")
        self.geometry("300x120")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()  # Make popup modal

        tk.Label(self, text="Username:", font=("Segoe UI", 10)).pack(pady=(10, 0))

        self.entry = tk.Entry(self, width=30)
        self.entry.pack(pady=5, padx=10)
        self.entry.focus_set()

        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="OK", width=10, command=self.submit).pack(side="left", padx=5)
        tk.Button(button_frame, text="Cancel", width=10, command=self.cancel).pack(side="left", padx=5)

        self.on_submit = on_submit

    def submit(self):
        username = self.entry.get().strip()
        if username:
            self.on_submit(username)
        self.destroy()

    def cancel(self):
        self.destroy()

# Example usage
def main():
    def handle_username(username):
        print("Username entered:", username)

    root = tk.Tk()
    root.withdraw()  # Hide main window if not needed
    UsernamePopup(root, handle_username)
    root.mainloop()

if __name__ == "__main__":
    main()
