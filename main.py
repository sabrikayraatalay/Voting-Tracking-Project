import tkinter as tk

# Correct way: from folder.filename import ClassName
from gui.LoginScreen import LoginScreen
from database import DatabaseManager


def main():
    # Initialize database
    db = DatabaseManager()

    # Create main window
    root = tk.Tk()

    # Instantiate the LoginScreen CLASS, not the module
    app = LoginScreen(root, db)

    # Start the application loop
    root.mainloop()

    # Close connection upon exit
    db.close_connection()


if __name__ == "__main__":
    main()