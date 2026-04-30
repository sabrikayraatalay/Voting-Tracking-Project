import tkinter as tk
from tkinter import messagebox, simpledialog
from models.Admin import Admin
from gui.BallotScreen import BallotScreen
from gui.AddCandidateScreen import AddCandidateScreen
from gui.ResultScreen import ResultScreen
from gui.CandidateListScreen import CandidateListScreen
from gui.AddPartyScreen import AddPartyScreen

# Tasarım Sabitleri
BG = "#EAECF0"
ACCENT = "#1A3A5C"
ACCENT_LIT = "#2E5F8A"
GOLD = "#C8963E"
GOLD_LIT = "#B8852E"
GREEN = "#2C6B4F"
GREEN_LIT = "#235940"
GRAY = "#6E6E73"
GRAY_LIT = "#555555"
FONT = "Arial"


def make_button(parent, text, command, bg, hover_bg):
    """Modern görünümlü buton oluşturucu"""
    btn = tk.Label(parent, text=text, font=(FONT, 12, "bold"),
                   bg=bg, fg="white", cursor="hand2", padx=20, pady=12)
    btn.pack(fill="x", pady=5, padx=40)
    btn.bind("<Button-1>", lambda e: command())
    btn.bind("<Enter>", lambda e: btn.configure(bg=hover_bg))
    btn.bind("<Leave>", lambda e: btn.configure(bg=bg))


class DashboardScreen:
    def __init__(self, root, db_manager, user):
        self.root = root
        self.db = db_manager
        self.user = user

        self.root.title("Election System - Dashboard")
        self.root.configure(bg=BG)

        # Pencere Boyutu ve Ortalama
        sw = root.winfo_screenwidth()
        sh = root.winfo_screenheight()
        w, h = 500, 750
        root.geometry(f"{w}x{h}+{(sw - w) // 2}+{(sh - h) // 2}")

        self.setup_ui()

    def setup_ui(self):
        # Ekranı temizle (Yenileme için)
        for widget in self.root.winfo_children():
            widget.destroy()

        # Aktif seçimi veritabanından çek
        active_election = self.db.get_active_election()
        is_active = active_election is not None

        election_title = active_election["title"] if is_active else "No Active Election"
        status_text = "Active 🟢" if is_active else "Completed / Inactive 🔴"

        # --- ÜST PANEL ---
        header = tk.Frame(self.root, bg=BG)
        header.pack(fill="x", pady=20)

        tk.Label(header, text=f"Welcome, {self.user.get_name()}", font=(FONT, 12), bg=BG).pack()
        tk.Label(header, text=election_title, font=(FONT, 20, "bold"), fg=ACCENT, bg=BG).pack(pady=5)
        tk.Label(header, text=f"Election Status: {status_text}", font=(FONT, 12, "bold"),
                 fg=GREEN if is_active else "#D32F2F", bg=BG).pack()

        # --- BUTON PANELİ ---
        btn_frame = tk.Frame(self.root, bg=BG)
        btn_frame.pack(fill="both", expand=True)

        # 1. ORTAK: Aday Listesi
        make_button(btn_frame, "👥 View Registered Candidates", self.open_candidates, GRAY, GRAY_LIT)

        # 2. SEÇMEN ÖZEL PANELİ
        if not isinstance(self.user, Admin):
            tk.Label(btn_frame, text="Voting & Results", font=(FONT, 10, "bold"), bg=BG, fg="#888888").pack(
                pady=(10, 0))

            if is_active:
                # Cumhurbaşkanlığı Oy Butonu
                if self.user.get_has_voted_president():
                    make_button(btn_frame, "✅ Voted for President", lambda: None, "#4A4A4A", "#4A4A4A")
                else:
                    make_button(btn_frame, "🗳️ Vote for President", lambda: self.open_ballot("President"), ACCENT,
                                ACCENT_LIT)

                # Belediye Başkanlığı Oy Butonu
                if self.user.get_has_voted_mayor():
                    make_button(btn_frame, "✅ Voted for Mayor", lambda: None, "#4A4A4A", "#4A4A4A")
                else:
                    make_button(btn_frame, "🗳️ Vote for Mayor", lambda: self.open_ballot("Mayor"), ACCENT, ACCENT_LIT)

                # Sonuçlar Seçim Bitene Kadar Kapalı
                make_button(btn_frame, "📊 View Results (Locked)",
                            lambda: messagebox.showinfo("Info", "Wait for the election to end to see results!"),
                            GRAY, GRAY)
            else:
                # Seçim Yoksa veya Bittiyse
                make_button(btn_frame, "⛔ Voting Closed", lambda: None, "#4A4A4A", "#4A4A4A")
                make_button(btn_frame, "📊 View Final Results", self.show_results, GREEN, GREEN_LIT)

        # 3. ADMIN ÖZEL PANELİ
        if isinstance(self.user, Admin):
            tk.Label(btn_frame, text="Admin Management", font=(FONT, 10, "bold"), bg=BG, fg="#888888").pack(
                pady=(15, 0))

            make_button(btn_frame, "🚩 Add New Party", self.open_add_party, GOLD, GOLD_LIT)

            if is_active:
                make_button(btn_frame, "➕ Add New Candidate", self.open_add_candidate, GOLD, GOLD_LIT)
                make_button(btn_frame, "🛑 END CURRENT ELECTION", self.end_election_action, "#C62828", "#B71C1C")
            else:
                make_button(btn_frame, "➕ Add Candidate (Locked)",
                            lambda: messagebox.showwarning("Warning", "Start a new election first!"), GRAY, GRAY)

            make_button(btn_frame, "📊 View Live/Final Results", self.show_results, GREEN, GREEN_LIT)

            # YENİ SEÇİM BAŞLATMA BUTONU
            make_button(btn_frame, "🆕 START NEW ELECTION", self.start_new_election_action, "#3A5C8A", "#2E496E")

        # --- ALT PANEL (ÇIKIŞ) ---
        tk.Label(btn_frame, text="", bg=BG).pack(pady=5)
        make_button(btn_frame, "🚪 Logout", self.logout, "#D32F2F", "#B71C1C")

    # --- AKSİYONLAR ---
    def open_candidates(self):
        CandidateListScreen(self.root, self.db, self.user)

    def open_ballot(self, election_type):
        ballot_win = BallotScreen(self.root, self.db, self.user, election_type)
        self.root.wait_window(ballot_win.window)

        # Oy verdikten sonra nesneyi manuel güncelle (Arayüzde ✅ görünmesi için)
        if election_type == "President":
            self.user.mark_voted_president()
        else:
            self.user.mark_voted_mayor()

        self.setup_ui()

    def end_election_action(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to end the current election? This cannot be undone!"):
            self.db.end_election()
            messagebox.showinfo("Success", "The election has been successfully ended.")
            self.setup_ui()

    def start_new_election_action(self):
        new_title = simpledialog.askstring("New Election",
                                           "Enter the title for the new election\n(e.g., '2028 General Elections'):")

        if new_title:
            new_title = new_title.strip()
            if new_title:
                self.db.create_election(new_title)
                messagebox.showinfo("Success",
                                    f"'{new_title}' has started successfully!\nPrevious election is archived.")
                self.setup_ui()
            else:
                messagebox.showerror("Error", "Election title cannot be empty!")

    def open_add_party(self):
        AddPartyScreen(self.root, self.db)

    def open_add_candidate(self):
        AddCandidateScreen(self.root, self.db)

    def show_results(self):
        ResultScreen(self.root, self.db)

    def logout(self):
        from gui.LoginScreen import LoginScreen
        for widget in self.root.winfo_children():
            widget.destroy()
        LoginScreen(self.root, self.db)