import os
import tkinter as tk
from tkinter import messagebox

from cryptography import x509

from ca_utils import (
    create_intermediate_ca,
    create_root_ca,
    issue_certificate,
    load_cert,
    verify_certificate_chain,
)
from revoke_utils import check_revocation_status, revoke_certificate


root_key = None
root_cert = None
inter_key = None
inter_cert = None


class CADemoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mini CA Demo UI")
        self.geometry("520x380")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Mini CA Demo", font=("Arial", 16, "bold")).pack(pady=10)
        self.log_text = tk.Text(self, height=11, width=64, state="disabled", bg="#f0f0f0")
        self.log_text.pack(pady=10)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="1. Tao Root & Intermediate CA", command=self.setup_ca).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="2. Phat hanh User Cert", command=self.issue_cert).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(btn_frame, text="3. Kiem tra Chuoi Cert", command=self.verify_chain).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="4. Thu hoi User Cert", command=self.revoke_cert).grid(row=1, column=1, padx=5, pady=5)
        tk.Button(btn_frame, text="5. Kiem tra OCSP", command=self.ocsp_check).grid(row=2, column=0, columnspan=2, pady=5)

    def log(self, message):
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")

    def setup_ca(self):
        global root_key, root_cert, inter_key, inter_cert
        self.log("Tao Root CA...")
        root_key, root_cert = create_root_ca()
        self.log("Root CA tao xong")
        self.log("Tao Intermediate CA...")
        inter_key, inter_cert = create_intermediate_ca(root_key, root_cert)
        self.log("Intermediate CA tao xong")
        messagebox.showinfo("Thong bao", "Da tao Root va Intermediate CA thanh cong")

    def issue_cert(self):
        global inter_key, inter_cert
        if not inter_key or not inter_cert:
            messagebox.showerror("Loi", "Phai tao CA truoc khi phat hanh chung chi")
            return
        self.log("Phat hanh chung chi KANE...")
        issue_certificate(inter_key, inter_cert, {"common_name": "KANE", "org": "HUTECH Security", "country": "VN"})
        self.log("Da phat hanh: certs/KANE_cert.pem, certs/KANE_key.pem")
        messagebox.showinfo("Thong bao", "Phat hanh chung chi thanh cong")

    def verify_chain(self):
        cert_path = os.path.join("certs", "KANE_cert.pem")
        if not os.path.exists(cert_path):
            messagebox.showerror("Loi", "Chua co chung chi user de kiem tra")
            return
        chain = [
            load_cert(os.path.join("certs", "intermediate_cert.pem")),
            load_cert(os.path.join("certs", "root_ca_cert.pem")),
        ]
        valid = verify_certificate_chain(load_cert(cert_path), chain)
        self.log(f"Chuoi hop le: {valid}")
        messagebox.showinfo("Ket qua", f"Chuoi chung chi hop le: {valid}")

    def revoke_cert(self):
        paths = [
            os.path.join("certs", "KANE_cert.pem"),
            os.path.join("certs", "intermediate_cert.pem"),
            os.path.join("certs", "intermediate_key.pem"),
        ]
        if not all(os.path.exists(path) for path in paths):
            messagebox.showerror("Loi", "Thieu file chung chi hoac khoa de thu hoi")
            return
        revoke_certificate(paths[0], paths[1], paths[2], reason=x509.ReasonFlags.key_compromise)
        self.log("Da thu hoi chung chi KANE")
        messagebox.showinfo("Thong bao", "Chung chi da duoc thu hoi")

    def ocsp_check(self):
        cert_path = os.path.join("certs", "KANE_cert.pem")
        if not os.path.exists(cert_path):
            messagebox.showerror("Loi", "Chua co chung chi user de kiem tra OCSP")
            return
        revoked = check_revocation_status(cert_path)
        self.log(f"Trang thai OCSP: {'Da thu hoi' if revoked else 'Hop le'}")
        messagebox.showinfo("Ket qua OCSP", f"Trang thai: {'Da thu hoi' if revoked else 'Hop le'}")


if __name__ == "__main__":
    app = CADemoApp()
    app.mainloop()
