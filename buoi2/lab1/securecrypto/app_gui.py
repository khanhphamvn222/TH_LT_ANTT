import tkinter as tk
from tkinter import filedialog, messagebox

from securecrypto import aes_utils


def encrypt():
    file_path = filedialog.askopenfilename()
    if not file_path:
        return
    try:
        key = aes_utils.encrypt_file_aes(file_path, password_entry.get())
        result_label.config(text=f"Key: {key}")
    except Exception as exc:
        messagebox.showerror("Encrypt failed", str(exc))


def decrypt():
    file_path = filedialog.askopenfilename()
    if not file_path:
        return
    try:
        output = aes_utils.decrypt_file_aes(file_path, password_entry.get())
        result_label.config(text=f"Output: {output}")
    except Exception as exc:
        messagebox.showerror("Decrypt failed", str(exc))


root = tk.Tk()
root.title("SecureCrypto GUI")

tk.Label(root, text="Password / key").pack(padx=12, pady=(12, 4))
password_entry = tk.Entry(root, show="*", width=52)
password_entry.pack(padx=12)
tk.Button(root, text="Encrypt", command=encrypt).pack(pady=(12, 4))
tk.Button(root, text="Decrypt", command=decrypt).pack(pady=4)
result_label = tk.Label(root, text="", wraplength=480, justify="left")
result_label.pack(padx=12, pady=12)


if __name__ == "__main__":
    root.mainloop()
