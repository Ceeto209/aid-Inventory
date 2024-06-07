import sqlite3

def view_inventory():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM inventory")
    rows = cursor.fetchall()
    conn.close()
    return rows

# Example usage:
# inventory = view_inventory()
# print(inventory)
