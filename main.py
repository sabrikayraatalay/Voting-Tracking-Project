
import tkinter as tk
from gui.LoginScreen import LoginScreen
from database import DatabaseManager

def main():
    db = DatabaseManager()
    root = tk.Tk()
    app = LoginScreen(root, db)
    root.mainloop()
    db.close_connection()

if __name__ == "__main__":
    main()
