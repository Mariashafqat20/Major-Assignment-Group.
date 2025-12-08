import tkinter as tk
from tkinter import ttk

class InventoryUI:
    def __init__(self, root, db):
        self.root = root
        self.db = db
        self.root.title("Smart Inventory System")
        self.root.geometry("1000x600")
        self.root.configure(bg="#f0f0f0")
        self.var_id = tk.StringVar()
        self.var_name = tk.StringVar()
        self.var_category = tk.StringVar()
        self.var_quantity = tk.StringVar()
        self.var_price = tk.StringVar()
        self.var_search = tk.StringVar()

        self.setup_ui()
            def setup_ui(self):
        # Title
        title = tk.Label(self.root, text="Smart Inventory System", font=("Helvetica", 24, "bold"), bg="#2c3e50", fg="white")
        title.pack(side=tk.TOP, fill=tk.X)
