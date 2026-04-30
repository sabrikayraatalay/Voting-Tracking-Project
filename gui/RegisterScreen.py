import tkinter as tk
from tkinter import messagebox, ttk
from models.Voter import Voter

# Sistem genelindeki sabit şehirler
CITIES = ["Ankara", "Istanbul", "Izmir", "Bursa", "Antalya", "Adana", "Konya"]


class RegisterScreen:
    def __init__(self, root, db_manager):
        self.root = root
        self.db = db_manager

        self.root.title("Election System - User Registration")
        self.root.geometry("400x550")
        self.root.configure(bg="#EAECF0")

        self.setup_ui()

    def setup_ui(self):
        # Başlık
        tk.Label(self.root, text="Create New Account", font=("Arial", 18, "bold"),
                 bg="#EAECF0", fg="#1A3A5C").pack(pady=30)

        # Form Alanları
        container = tk.Frame(self.root, bg="#EAECF0")
        container.pack(padx=40, fill="x")

        # TC No
        tk.Label(container, text="TC Identification Number:", bg="#EAECF0").pack(anchor="w")
        self.tc_entry = tk.Entry(container, font=("Arial", 11))
        self.tc_entry.pack(fill="x", pady=(0, 15))

        # İsim Soyisim
        tk.Label(container, text="Full Name:", bg="#EAECF0").pack(anchor="w")
        self.name_entry = tk.Entry(container, font=("Arial", 11))
        self.name_entry.pack(fill="x", pady=(0, 15))

        # Şehir Seçimi (YENİ: Combobox)
        tk.Label(container, text="Select Your City:", bg="#EAECF0").pack(anchor="w")
        self.city_combo = ttk.Combobox(container, values=CITIES, state="readonly", font=("Arial", 10))
        self.city_combo.set("Select City")  # Varsayılan metin
        self.city_combo.pack(fill="x", pady=(0, 15))

        # Şifre
        tk.Label(container, text="Password:", bg="#EAECF0").pack(anchor="w")
        self.pass_entry = tk.Entry(container, font=("Arial", 11), show="*")
        self.pass_entry.pack(fill="x", pady=(0, 20))

        # Kayıt Butonu
        tk.Button(self.root, text="REGISTER", bg="#1A3A5C", fg="white", font=("Arial", 12, "bold"),
                  command=self.register_user, pady=10).pack(fill="x", padx=40, pady=10)

        # Geri Dön
        tk.Button(self.root, text="Back to Login", fg="#1A3A5C", bg="#EAECF0", bd=0,
                  cursor="hand2", command=self.back_to_login).pack()

    def register_user(self):
        tc = self.tc_entry.get().strip()
        name = self.name_entry.get().strip()
        city = self.city_combo.get()
        password = self.pass_entry.get().strip()

        # Validasyonlar
        if not (tc and name and password) or city == "Select City":
            messagebox.showwarning("Warning", "All fields are required!")
            return

        if len(tc) != 11 or not tc.isdigit():
            messagebox.showerror("Error", "TC Number must be 11 digits!")
            return

        # OOP: Yeni bir seçmen nesnesi oluştur
        new_voter = Voter(tc, name, password, city)

        if self.db.register_user(new_voter):
            messagebox.showinfo("Success", "Registration successful! You can now login.")
            self.back_to_login()
        else:
            messagebox.showerror("Error", "TC Number already registered!")

    def back_to_login(self):
        from gui.LoginScreen import LoginScreen
        for widget in self.root.winfo_children():
            widget.destroy()
        LoginScreen(self.root, self.db)