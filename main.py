import tkinter as tk
from db import DBManager
from gui import AppGUI

if __name__ == "__main__":
    db_params = {
        'host': 'localhost',
        'user': 'admin',
        'password': 'passwd',
        'database': 'shoes_db'
    }
    db_manager = DBManager(**db_params)
    db_manager.connect()
    root = tk.Tk()
    app = AppGUI(root, db_manager)
    root.mainloop()
    db_manager.disconnect()