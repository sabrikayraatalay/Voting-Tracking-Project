import tkinter as tk
from tkinter import messagebox

# ── Design Tokens ─────────────────────────────────────────────────────────────
BG         = "#EAECF0"
CARD_BG    = "#FFFFFF"
ACCENT     = "#1A3A5C"
ACCENT_LIT = "#2E5F8A"
TEXT_PRI   = "#1C1C1E"
TEXT_SEC   = "#6E6E73"
BORDER     = "#C8C8CC"
SUCCESS    = "#34C759"
SUCCESS_LT = "#2CA048"
FONT       = "Helvetica Neue"
# ─────────────────────────────────────────────────────────────────────────────


class BallotScreen:
    def __init__(self, parent, db_manager, current_user):
        self.window = tk.Toplevel(parent)
        self.db     = db_manager
        self.user   = current_user

        self.window.title("Official Election Ballot")
        self.window.configure(bg=BG)
        self.window.resizable(False, False)

        sw = self.window.winfo_screenwidth()
        sh = self.window.winfo_screenheight()
        w, h = 460, 560
        self.window.geometry(f"{w}x{h}+{(sw - w) // 2}+{(sh - h) // 2}")

        self.window.grab_set()
        self.setup_ui()

    def setup_ui(self):
        # Header
        header = tk.Frame(self.window, bg=ACCENT)
        header.pack(fill="x")
        tk.Label(header, text="📋  Official Ballot",
                 font=(FONT, 15, "bold"), bg=ACCENT, fg="white"
                 ).pack(pady=(18, 2))
        tk.Label(header, text="Select one candidate and submit your vote",
                 font=(FONT, 10), bg=ACCENT, fg="#A8C0D8"
                 ).pack(pady=(0, 18))

        # Candidates
        self.candidates = self.db.get_all_candidates()

        list_frame = tk.Frame(self.window, bg=BG)
        list_frame.pack(fill="both", expand=True, padx=24, pady=18)

        if not self.candidates:
            tk.Label(list_frame, text="No candidates available at this time.",
                     font=(FONT, 12), bg=BG, fg=TEXT_SEC).pack(pady=30)
            return

        self.selected_id = tk.IntVar(value=0)
        self.rows = {}

        for c in self.candidates:
            self._candidate_row(list_frame, c)

        # Submit button (Label-based — macOS safe)
        btn_frame = tk.Frame(self.window, bg=BG)
        btn_frame.pack(fill="x", padx=24, pady=(0, 22))

        submit = tk.Label(btn_frame, text="  ✓   Submit Vote",
                          font=(FONT, 13, "bold"),
                          bg=SUCCESS, fg="white",
                          cursor="hand2", pady=13)
        submit.pack(fill="x")
        submit.bind("<Button-1>", lambda e: self.submit_vote())
        submit.bind("<Enter>",    lambda e: submit.configure(bg=SUCCESS_LT))
        submit.bind("<Leave>",    lambda e: submit.configure(bg=SUCCESS))

    def _candidate_row(self, parent, candidate):
        cid = candidate.get_candidate_id()

        row = tk.Frame(parent, bg=CARD_BG,
                       highlightthickness=1,
                       highlightbackground=BORDER)
        row.pack(fill="x", pady=5)
        self.rows[cid] = row

        rb = tk.Radiobutton(row,
                            variable=self.selected_id, value=cid,
                            bg=CARD_BG, activebackground=CARD_BG,
                            selectcolor=ACCENT,
                            cursor="hand2",
                            command=lambda c=cid: self._highlight(c))
        rb.pack(side="left", padx=(14, 4), pady=14)

        info = tk.Frame(row, bg=CARD_BG)
        info.pack(side="left", fill="both", expand=True, pady=10, padx=(0, 14))

        display = str(candidate)
        parts    = display.split("(", 1)
        name_txt = parts[0].strip()
        rest_txt = f"({parts[1].strip()}" if len(parts) > 1 else ""

        tk.Label(info, text=name_txt,
                 font=(FONT, 12, "bold"), bg=CARD_BG, fg=TEXT_PRI,
                 anchor="w").pack(fill="x")
        if rest_txt:
            tk.Label(info, text=rest_txt,
                     font=(FONT, 10), bg=CARD_BG, fg=TEXT_SEC,
                     anchor="w").pack(fill="x")

        for w in (row, info):
            w.bind("<Button-1>", lambda e, c=cid: self._select(c))

    def _select(self, cid):
        self.selected_id.set(cid)
        self._highlight(cid)

    def _highlight(self, selected_cid):
        for cid, row in self.rows.items():
            row.configure(
                highlightbackground=ACCENT if cid == selected_cid else BORDER
            )

    # ── Backend (unchanged) ───────────────────────────────────────────────────

    def submit_vote(self):
        candidate_id = self.selected_id.get()

        if candidate_id == 0:
            messagebox.showwarning("Warning",
                                   "Please select a candidate before submitting!",
                                   parent=self.window)
            return

        selected_c = next((c for c in self.candidates
                           if c.get_candidate_id() == candidate_id), None)
        position = selected_c.get_position()

        if position.lower() == "president" and self.user.get_has_voted_president():
            messagebox.showerror("Error",
                                 "You have already cast your vote for a President!",
                                 parent=self.window)
            return

        if position.lower() == "mayor" and self.user.get_has_voted_mayor():
            messagebox.showerror("Error",
                                 "You have already cast your vote for a Mayor!",
                                 parent=self.window)
            return

        self.db.cast_vote(self.user.get_tc_no(), candidate_id, position)

        if position.lower() == "president":
            self.user.mark_voted_president()
        else:
            self.user.mark_voted_mayor()

        messagebox.showinfo("Success",
                            "Your vote has been securely recorded!",
                            parent=self.window)
        self.window.destroy()
