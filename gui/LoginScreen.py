import tkinter as tk
from tkinter import messagebox
from gui.DashboardScreen import DashboardScreen

BG = "#EAECF0"
CARD_BG = "#FFFFFF"
ACCENT = "#1A3A5C"
ACCENT_LIT = "#2E5F8A"
TEXT_PRI = "#1C1C1E"
TEXT_SEC = "#6E6E73"
BORDER = "#C8C8CC"
FONT = "Arial"


def make_button(parent, text, command, bg, hover_bg):
    btn = tk.Label(parent, text=text,
                   font=(FONT, 13, "bold"),
                   bg=bg, fg="white",
                   cursor="hand2",
                   pady=13)
    btn.pack(fill="x")
    btn.bind("<Button-1>", lambda e: command())
    btn.bind("<Enter>", lambda e: btn.configure(bg=hover_bg))
    btn.bind("<Leave>", lambda e: btn.configure(bg=bg))
    return btn


class LoginScreen:
    def __init__(self, root, db_manager):
        self.root = root
        self.db = db_manager

        self.root.title("Election System - Login")
        self.root.configure(bg=BG)

        # 1. MAC BUG FIX: Ekran çizilene kadar pencereyi tamamen gizle
        self.root.withdraw()

        # 2. Monitör boyutunu al ve ekranı tam ortaya konumlandır
        # (Bu komutlar UI çizilmeden önce de çalışır, beklememize gerek yok)
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        w, h = 400, 420
        self.root.geometry(f"{w}x{h}+{(sw - w)//2}+{(sh - h)//2}")
        self.root.resizable(False, False)

        # 3. UI elemanlarını (butonlar, kutular vs.) pencereye yerleştir
        self.setup_ui()

        # 4. Güvenli Çizim: İşletim sistemi olaylarını dinlemeden SADECE çizimi güncelle
        self.root.update_idletasks()

        # 5. Her şey hazır! Gizlediğimiz pencereyi tüm ihtişamıyla ekrana getir
        self.root.deiconify()

    def setup_ui(self):
        hero = tk.Frame(self.root, bg=ACCENT)
        hero.pack(fill="x")

        tk.Label(hero, text="Election System",
                 font=(FONT, 17, "bold"),
                 bg=ACCENT, fg="white").pack(pady=(24, 4))

        tk.Label(hero, text="Secure Voting Platform",
                 font=(FONT, 10),
                 bg=ACCENT, fg="#A8C0D8").pack(pady=(0, 20))

        form = tk.Frame(self.root, bg=BG)
        form.pack(fill="x", padx=36, pady=20)

        tk.Label(form, text="TC Identity Number",
                 font=(FONT, 11, "bold"),
                 bg=BG, fg=TEXT_SEC).pack(anchor="w")

        self.tc_entry = tk.Entry(form, font=(FONT, 12))
        self.tc_entry.pack(fill="x", pady=6)

        tk.Label(form, text="Password",
                 font=(FONT, 11, "bold"),
                 bg=BG, fg=TEXT_SEC).pack(anchor="w")

        self.pass_entry = tk.Entry(form, show="*", font=(FONT, 12))
        self.pass_entry.pack(fill="x", pady=6)

        make_button(form, "Sign In",
                    self.attempt_login, ACCENT, ACCENT_LIT)

    def attempt_login(self):
        tc = self.tc_entry.get().strip()
        password = self.pass_entry.get().strip()

        if not tc or not password:
            messagebox.showwarning("Warning", "Please fill all fields.")
            return

        user = self.db.authenticate_user(tc, password)

        if user:
            # 3. Hide root instead of destroying to keep DB connection alive
            self.root.withdraw()
            self.open_dashboard(user)
        else:
            messagebox.showerror("Error", "Invalid credentials.")

    def open_dashboard(self, user):
        # 4. Use Toplevel to prevent new mainloop clashes
        dash_window = tk.Toplevel(self.root)
        dash_window.protocol("WM_DELETE_WINDOW", lambda: self.root.destroy())
        DashboardScreen(dash_window, self.db, user)