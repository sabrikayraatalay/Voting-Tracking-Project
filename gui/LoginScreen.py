import tkinter as tk
from tkinter import messagebox

# Tasarım Sabitleri (Dashboard ile uyumlu)
BG = "#EAECF0"
ACCENT = "#1A3A5C"
FONT = "Arial"


class LoginScreen:
    def __init__(self, root, db_manager):
        self.root = root
        self.db = db_manager

        self.root.title("Election System - Login")
        self.root.configure(bg=BG)

        # Pencere Boyutu ve Ortalama
        sw = root.winfo_screenwidth()
        sh = root.winfo_screenheight()
        w, h = 400, 500
        root.geometry(f"{w}x{h}+{(sw - w) // 2}+{(sh - h) // 2}")

        self.setup_ui()

    def setup_ui(self):
        # Ekranı temizle
        for widget in self.root.winfo_children():
            widget.destroy()

        # Logo veya İkon Alanı (Opsiyonel)
        tk.Label(self.root, text="🗳️", font=(FONT, 50), bg=BG).pack(pady=(40, 10))

        tk.Label(self.root, text="Secure Voting System", font=(FONT, 18, "bold"),
                 fg=ACCENT, bg=BG).pack(pady=10)

        # Giriş Formu
        form_frame = tk.Frame(self.root, bg=BG)
        form_frame.pack(pady=20, padx=50, fill="x")

        tk.Label(form_frame, text="TC Number:", font=(FONT, 10), bg=BG).pack(anchor="w")
        self.tc_entry = tk.Entry(form_frame, font=(FONT, 12), bd=1, relief="solid")
        self.tc_entry.pack(fill="x", pady=(5, 15))

        tk.Label(form_frame, text="Password:", font=(FONT, 10), bg=BG).pack(anchor="w")
        self.pass_entry = tk.Entry(form_frame, font=(FONT, 12), bd=1, relief="solid", show="*")
        self.pass_entry.pack(fill="x", pady=(5, 10))

        # Giriş Butonu
        login_btn = tk.Button(self.root, text="LOGIN", font=(FONT, 12, "bold"),
                              bg=ACCENT, fg="white", cursor="hand2",
                              command=self.login_action, pady=10)
        login_btn.pack(fill="x", padx=50, pady=10)

        # KAYIT OLMA BUTONU (Hatanın düzeltildiği yer)
        register_link = tk.Label(self.root, text="Don't have an account? Register New Account",
                                 font=(FONT, 9, "underline"), fg=ACCENT, bg=BG, cursor="hand2")
        register_link.pack(pady=10)
        register_link.bind("<Button-1>", lambda e: self.open_register())

    def login_action(self):
        tc = self.tc_entry.get().strip()
        password = self.pass_entry.get().strip()

        if not tc or not password:
            messagebox.showwarning("Warning", "Please enter both TC and Password!")
            return

        user = self.db.authenticate_user(tc, password)

        if user:
            from gui.DashboardScreen import DashboardScreen
            # Giriş başarılı, dashboard'a geç
            DashboardScreen(self.root, self.db, user)
        else:
            messagebox.showerror("Error", "Invalid TC Number or Password!")

    def open_register(self):
        """Kayıt ekranını açar ve mevcut ekranı temizler."""
        from gui.RegisterScreen import RegisterScreen  # Metot içi import (Döngüsel hatayı engeller)

        # Ekranı temizle
        for widget in self.root.winfo_children():
            widget.destroy()

        # Yeni ekranı başlat
        RegisterScreen(self.root, self.db)