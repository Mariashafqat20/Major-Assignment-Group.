# ...existing code...
import tkinter as tk
from gul_andam_backend.database import InventoryDB

from ui import InventoryUI

if __name__ == "__main__":
    # 1. Initialize Database
    db = InventoryDB()
    
    # 2. Setup Main Window
    root = tk.Tk()
    
    # 3. Connect UI to Database
    app = InventoryUI(root, db)
    
    # 4. Load Initial Data (ensure UI shows data on startup)
    app.fetch_data()
    
    # 5. Start App
    root.mainloop()
# ...existing code...