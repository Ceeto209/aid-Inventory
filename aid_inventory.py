from database import setup_database, add_item_to_inventory, delete_item_from_inventory, view_inventory, delete_inventory_by_item
from excel import extract_characters_from_csv, extract_items_to_delete_from_csv
import logging
import csv
import gui
import excel
import database

def add_inventory_from_csv(file_path, column_name):
    try:
        characters = extract_characters_from_csv(file_path, column_name)
        for character in characters:
            add_item_to_inventory(character)
        logging.info("Inventory added successfully from CSV file: %s", file_path)
    except Exception as e:
        logging.error("Error adding inventory from CSV file %s: %s", file_path, str(e))

# Setup database
setup_database()

# Example usage:

# file_path = 'A:\\CODING PROJECTS\\aid-Inventory\\scans\\scan7.csv'
# column_name = 'AID'
# add_inventory_from_csv(file_path, column_name)


# delete_path =
def delete_inventory_from_csv(file_path, column_name):
    try:
        items_to_delete = extract_items_to_delete_from_csv(file_path, column_name)
        for item in items_to_delete:
            delete_item_from_inventory(item)
        logging.info("Inventory deleted successfully based on criteria in CSV file: %s", file_path)
    except Exception as e:
        logging.error("Error deleting inventory based on criteria in CSV file %s: %s", file_path, str(e))




logging.basicConfig(filename='inventory.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')




# for csv export files
def export_inventory_to_csv(file_path):
    inventory = view_inventory()
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Item', 'AID#'])
        for item in inventory:
            writer.writerow(item)
