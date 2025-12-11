import tkinter as tk
from tkinter import ttk

class InventoryUI:
    def __init__(self, root, db):
        self.root = root                # Main application window
        self.db = db                    # Database connection object
        self.root.title("Smart Inventory System")
        self.root.geometry("1000x600")  # Set app window size
        self.root.configure(bg="#f0f0f0")  # Background color

        # Tkinter Variables for form fields
        self.var_id = tk.StringVar()        # Stores selected product ID
        self.var_name = tk.StringVar()      # Product Name
        self.var_category = tk.StringVar()  # Product Category
        self.var_quantity = tk.StringVar()  # Product Quantity
        self.var_price = tk.StringVar()     # Product Price
        self.var_search = tk.StringVar()    # Search input

        self.setup_ui()  # Build UI

    def setup_ui(self):
        # -------------------- TITLE BAR --------------------
        title = tk.Label(
            self.root, text="Smart Inventory System",
            font=("Helvetica", 24, "bold"),
            bg="#2c3e50", fg="white"
        )
        title.pack(side=tk.TOP, fill=tk.X)

        # -------------------- INPUT FRAME -------------------
        input_frame = tk.Frame(self.root, bd=4, relief=tk.RIDGE, bg="white")
        input_frame.place(x=20, y=70, width=400, height=500)

        # Labels and entry field setup
        labels = ["Name", "Category", "Quantity", "Price"]
        variables = [self.var_name, self.var_category, self.var_quantity, self.var_price]

        # Loop to generate labels + input boxes
        for i, text in enumerate(labels):
            tk.Label(input_frame, text=text, font=("Arial", 12), bg="white") \
                .grid(row=i, column=0, pady=10, padx=20, sticky="w")

            tk.Entry(input_frame, textvariable=variables[i], font=("Arial", 12),
                     bd=2, relief=tk.GROOVE) \
                .grid(row=i, column=1, pady=10, padx=20)

        # -------------------- BUTTON FRAME --------------------
        btn_frame = tk.Frame(input_frame, bg="white")
        btn_frame.place(x=10, y=350, width=380)

        # List of buttons: (Label, Color, Function)
        buttons = [
            ("Add", "#27ae60", self.add_data),
            ("Update", "#2980b9", self.update_data),
            ("Delete", "#c0392b", self.delete_data),
            ("Clear", "#7f8c8d", self.clear_form)
        ]

        # Generate buttons using loop
        for i, (text, color, cmd) in enumerate(buttons):
            tk.Button(
                btn_frame, text=text, command=cmd,
                bg=color, fg="white",
                font=("Arial", 10, "bold"), width=8
            ).grid(row=0, column=i, padx=5)

        # -------------------- DISPLAY FRAME --------------------
        display_frame = tk.Frame(self.root, bd=4, relief=tk.RIDGE, bg="white")
        display_frame.place(x=440, y=70, width=540, height=500)

        # Search Label + Entry + Buttons
        tk.Label(display_frame, text="Search:", bg="white", font=("Arial", 11)) \
            .grid(row=0, column=0, padx=10, pady=10)

        tk.Entry(display_frame, textvariable=self.var_search,
                 width=15, font=("Arial", 11)) \
            .grid(row=0, column=1, padx=10, pady=10)

        tk.Button(display_frame, text="Search", command=self.search_data,
                  bg="#8e44ad", fg="white") \
            .grid(row=0, column=2, padx=10)

        tk.Button(display_frame, text="Show All", command=self.fetch_data,
                  bg="#34495e", fg="white") \
            .grid(row=0, column=3, padx=10)

        # -------------------- PRODUCT TABLE --------------------
        self.product_table = ttk.Treeview(
            display_frame,
            columns=("ID", "Name", "Category", "Qty", "Price"),
            show="headings"
        )

        # Set column widths + headings
        col_widths = [40, 140, 100, 70, 70]
        headers = ["ID", "Name", "Category", "Qty", "Price"]

        for col, width, head in zip(self.product_table["columns"], col_widths, headers):
            self.product_table.heading(col, text=head)
            self.product_table.column(col, width=width)

        self.product_table.place(x=10, y=60, width=515, height=420)

        # Bind row selection event
        self.product_table.bind("<ButtonRelease-1>", self.get_cursor)

        # Red text for low stock rows (Quantity < 5)
        self.product_table.tag_configure('low_stock', foreground='red')

    # ==========================================================
    #                     BUTTON LOGIC
    # ==========================================================

    def add_data(self):
        # Validation: Name cannot be empty
        if self.var_name.get().strip() == "":
            from tkinter import messagebox
            messagebox.showerror("Error", "Name is required")
            return

        try:
            # Add product into database
            self.db.add_product(
                self.var_name.get(),
                self.var_category.get(),
                int(self.var_quantity.get()),
                float(self.var_price.get())
            )

            self.fetch_data()  # Refresh table
            self.clear_form()  # Clear input fields

            from tkinter import messagebox
            messagebox.showinfo("Success", "Product Added")

        except ValueError:
            # User entered invalid number inputs
            from tkinter import messagebox
            messagebox.showerror("Error", "Quantity must be integer and Price must be number")

    def fetch_data(self):
        # Clear old table rows
        for item in self.product_table.get_children():
            self.product_table.delete(item)

        # Fetch all products from DB
        rows = self.db.fetch_all()

        # Insert records into table
        for row in rows:
            if int(row[3]) < 5:  # Quantity < 5 = show in red
                self.product_table.insert('', tk.END, values=row, tags=('low_stock',))
            else:
                self.product_table.insert('', tk.END, values=row)

    def update_data(self):
        # Must select an item to update
        if self.var_id.get().strip() == "":
            from tkinter import messagebox
            messagebox.showerror("Error", "Select a product to update")
            return

        # Update DB entry
        self.db.update_product(
            int(self.var_id.get()),
            self.var_name.get(),
            self.var_category.get(),
            int(self.var_quantity.get()),
            float(self.var_price.get())
        )

        self.fetch_data()  # Refresh table
        self.clear_form()  # Clear fields

        from tkinter import messagebox
        messagebox.showinfo("Success", "Product Updated")

    def delete_data(self):
        # Must select an item to delete
        if self.var_id.get().strip() == "":
            from tkinter import messagebox
            messagebox.showerror("Error", "Select a product to delete")
            return

        self.db.delete_product(int(self.var_id.get()))
        self.fetch_data()
        self.clear_form()

    def search_data(self):
        # Clear previous results
        for item in self.product_table.get_children():
            self.product_table.delete(item)

        # Search DB
        rows = self.db.search_product(self.var_search.get())

        # Show search results
        for row in rows:
            self.product_table.insert('', tk.END, values=row)

    def clear_form(self):
        # Reset all input fields
        self.var_id.set("")
        self.var_name.set("")
        self.var_category.set("")
        self.var_quantity.set("")
        self.var_price.set("")

    def get_cursor(self, event):
        # Get selected table row values
        cursor_row = self.product_table.focus()
        contents = self.product_table.item(cursor_row)
        row = contents.get('values', [])

        # Fill form with selected row data
        if row:
            self.var_id.set(row[0])
            self.var_name.set(row[1])
            self.var_category.set(row[2])
            self.var_quantity.set(row[3])
            self.var_price.set(row[4])
