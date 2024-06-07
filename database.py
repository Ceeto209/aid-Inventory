import sqlite3

def setup_database():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS inventory (
                        id INTEGER PRIMARY KEY,
                        item TEXT
                        )''')
    conn.commit()
    conn.close()

def add_item_to_inventory(item):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO inventory (item) VALUES (?)", (item,))
    conn.commit()
    conn.close()

def delete_item_from_inventory(item):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM inventory WHERE item=?", (item,))
    conn.commit()
    conn.close()

def delete_inventory_by_item(item):
    conn = sqlite3.connect("inventory.db")
    c = conn.cursor()
    c.execute("DELETE FROM inventory WHERE item = ?", (item,))
    conn.commit()
    conn.close()


def view_inventory():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM inventory")
    rows = cursor.fetchall()
    conn.close()

    # Manually assign sequential numbers to the items
    numbered_rows = [(i + 1,) + row[1:] for i, row in enumerate(rows)]

    return numbered_rows
