import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
from aid_inventory import add_inventory_from_csv, delete_inventory_from_csv, view_inventory, delete_inventory_by_item, export_inventory_to_csv

class InventoryApp:
    def __init__(self, master):
        self.master = master
        master.title("Inventory Management")

        # Create frame to contain buttons, search box, and treeview
        self.frame = ttk.Frame(master)
        self.frame.pack(fill=tk.BOTH, expand=True)



        # Add search box
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(self.frame, textvariable=self.search_var)
        self.search_entry.pack(side=tk.TOP, fill=tk.X)
        self.search_entry.bind("<KeyRelease>", self.search_inventory)

        # Add Treeview
        self.tree = ttk.Treeview(self.frame, columns=("AID", "Item"), show="headings")
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add scrollbars
        self.tree_scroll = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=self.tree_scroll.set)

        # Configure Treeview columns
        self.tree.heading("AID", text="AID")
        self.tree.heading("Item", text="Item")

        # Add buttons
        self.add_button = tk.Button(master, text="Add Inventory", command=self.add_inventory)
        self.add_button.pack(side=tk.LEFT)

        self.delete_button = tk.Button(master, text="Delete Inventory", command=self.delete_inventory)
        self.delete_button.pack(side=tk.LEFT)

        self.export_button = tk.Button(master, text="Export Inventory", command=self.export_inventory)
        self.export_button.pack(side=tk.LEFT)

        # Add total label
        self.total_label = tk.Label(master, text="")
        self.total_label.pack(side=tk.RIGHT)

        # Populate Treeview
        self.populate_tree()

        # Delete selected
        self.delete_selected_button = tk.Button(master, text="Delete Selected", command=self.delete_selected)
        self.delete_selected_button.pack(side=tk.LEFT)

        # Create a custom style for the Treeview
        style = ttk.Style(root)
        # style.configure("Treeview", borderwidth=1, relief="solid", color="#dddd")
        style.configure("Border.Treeview", padding=10, relief="flat", background="#ccc")

        self.tree.tag_configure("outline", background="#dddddd")

        # Apply the custom style to the Treeview
        self.tree.config(style="Treeview")
        self.tree.config(style="Border.Treeview")

    def populate_tree(self):
        # Clear existing items from the Treeview
        self.tree.delete(*self.tree.get_children())
        # Fetch updated inventory from the database
        inventory = view_inventory()
        # Insert updated inventory into the Treeview
        for item in inventory:
            self.tree.insert("", "end", values=item, tags=("outline",))
        # Update total label
        total_items = len(inventory)
        self.total_label.config(text=f"Total items: {total_items}")

    def add_inventory(self):
        # Ask for confirmation before adding inventory
        confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to add inventory?")
        if confirmation:
            file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
            if file_path:
                add_inventory_from_csv(file_path, 'AID')
                count_added = len(self.tree.selection())
                self.tree.delete(*self.tree.get_children())
                self.populate_tree()
                # Display popup with the number of items added
                messagebox.showinfo("Items Added", f"{count_added} items added.")

    def confirm_delete_inventory(self):
        # Get the number of items to be deleted
        items_to_delete = len(self.tree.selection())
        if items_to_delete > 0:
            # Ask for confirmation before deleting inventory
            confirmation = messagebox.askyesno("Confirmation",
                                               f"Are you sure you want to delete {items_to_delete} item(s)?")
            if confirmation:
                self.delete_inventory()
    def delete_inventory(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            count_deleted = delete_inventory_from_csv(file_path, 'AID')
            self.tree.delete(*self.tree.get_children())
            self.populate_tree()
            # Display popup with the number of items deleted
            messagebox.showinfo("Items Deleted", f"{count_deleted} items deleted.")

    def delete_selected(self):
        selected_items = self.tree.selection()
        for item_id in selected_items:
            item = self.tree.item(item_id)["values"][1]  # Get the item value from the Treeview
            delete_inventory_by_item(item)
        self.tree.delete(*selected_items)
        self.populate_tree()

    def search_inventory(self, event=None):
        search_query = self.search_var.get().lower()
        self.tree.delete(*self.tree.get_children())
        for item in view_inventory():
            # Check if the search query is present in any part of the AID or item string
            if any(search_query in str(value).lower() for value in item):
                self.tree.insert("", "end", values=item)

    def export_inventory(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            export_inventory_to_csv(file_path)



root = tk.Tk()
app = InventoryApp(root)
root.mainloop()
