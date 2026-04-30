import tkinter as tk
from tkinter import messagebox

# Tasarım Sabitleri
BG = "#EAECF0"
CARD_BG = "#FFFFFF"
BORDER = "#C8C8CC"
SUCCESS = "#2C6B4F"
FONT = "Arial"


class BallotScreen:
    # YENİ: election_type parametresi eklendi
    def __init__(self, parent, db, user, election_type):
        self.window = tk.Toplevel(parent)
        self.db = db
        self.user = user
        self.election_type = election_type  # "President" veya "Mayor"

        self.window.title(f"Voting Ballot - {self.election_type}")
        self.window.geometry("500x600")
        self.window.configure(bg=BG)

        self.selected_id = tk.IntVar(value=0)
        self.setup_ui()

    def setup_ui(self):
        # Başlığı dinamik yaptık
        tk.Label(self.window, text=f"Cast Your Vote for {self.election_type}",
                 font=(FONT, 18, "bold"), bg=BG).pack(pady=20)

        candidates = self.db.get_all_candidates()

        container = tk.Frame(self.window, bg=BG)
        container.pack(fill="both", expand=True, padx=20)

        has_candidates = False
        for c in candidates:
            # Sadece seçilen seçim türüne (President/Mayor) ait adayları göster
            if c.get_position() == self.election_type:
                # Eğer Belediye Başkanı ise, kullanıcının şehriyle eşleşenleri göster
                if self.election_type == "President" or c.get_city() == self.user.get_city():
                    self.create_candidate_row(container, c)
                    has_candidates = True

        if not has_candidates:
            tk.Label(container, text=f"No candidates found for {self.election_type} in your area.",
                     bg=BG, fg="red", font=(FONT, 10, "italic")).pack(pady=20)

        tk.Button(self.window, text="SUBMIT VOTE", bg=SUCCESS, fg="white",
                  font=(FONT, 12, "bold"), command=self.submit_vote, pady=10).pack(fill="x", padx=50, pady=20)

    def create_candidate_row(self, parent, c):
        frame = tk.Frame(parent, bg=CARD_BG, highlightthickness=1, highlightbackground=BORDER)
        frame.pack(fill="x", pady=5, ipady=5)

        tk.Radiobutton(frame, variable=self.selected_id, value=c.get_candidate_id(), bg=CARD_BG).pack(side="left",
                                                                                                      padx=10)

        info = f"{c.get_name()} ({c.get_party()})"
        tk.Label(frame, text=info, font=(FONT, 11), bg=CARD_BG).pack(side="left")

    def submit_vote(self):
        cid = self.selected_id.get()
        if cid == 0:
            messagebox.showwarning("Warning", "Please select a candidate!")
            return

        # Zaten oy verildiyse güvenlik kontrolü (Dashboard engelliyor ama çift dikiş atalım)
        if self.election_type == "President" and self.user.get_has_voted_president():
            messagebox.showerror("Error", "You have already voted for President!")
            self.window.destroy()
            return

        if self.election_type == "Mayor" and self.user.get_has_voted_mayor():
            messagebox.showerror("Error", "You have already voted for Mayor!")
            self.window.destroy()
            return

        # Oyu kaydet
        if self.db.cast_vote(self.user.get_tc_no(), cid, self.election_type):
            if self.election_type == "President":
                self.user.mark_voted_president()
            else:
                self.user.mark_voted_mayor()

            messagebox.showinfo("Success", f"Your vote for {self.election_type} has been recorded securely.")
            self.window.destroy()