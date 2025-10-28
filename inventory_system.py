
"""Inventory management system with safe and clean code."""
import json
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def add_item(stock_data, item="default", qty=0, logs=None):
    """Add an item to inventory safely."""
    if logs is None:
        logs = []

    if not isinstance(item, str) or not isinstance(qty, (int, float)):
        logging.warning("Invalid input for add_item: item=%s, qty=%s", item, qty)
        return stock_data, logs

    stock_data[item] = stock_data.get(item, 0) + qty
    logs.append(f"{datetime.now()}: Added {qty} of {item}")
    return stock_data, logs

def remove_item(stock_data, item, qty):
    """Remove quantity from an item."""
    try:
        if item not in stock_data:
            logging.warning("Tried to remove non-existent item: %s", item)
            return stock_data
        stock_data[item] -= qty
        if stock_data[item] <= 0:
            del stock_data[item]
    except KeyError as e:
        logging.error("Key error: %s", e)
    except (OSError, ValueError) as e:
        logging.error("Error removing item: %s", e)
    return stock_data

def get_qty(stock_data, item):
    """Return quantity of given item."""
    return stock_data.get(item, 0)

def load_data(file_path="inventory.json"):
    """Load stock data from JSON file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            logging.info("Data loaded from %s", file_path)
            return data
    except FileNotFoundError:
        logging.warning("File not found: starting with empty inventory.")
        return {}
    except json.JSONDecodeError as e:
        logging.error("Invalid JSON in %s: %s", file_path, e)
        return {}

def save_data(file_path="inventory.json", data=None):
    """Save stock data to JSON file."""
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
            logging.info("Data saved to %s", file_path)
    except (OSError, TypeError) as e:
        logging.error("Error saving data: %s", e)

def print_data(stock_data):
    """Print all items."""
    print("Items Report:")
    for item, qty in stock_data.items():
        print(f"{item} -> {qty}")

def check_low_items(stock_data, threshold=5):
    """Return list of low-stock items."""
    return [item for item, qty in stock_data.items() if qty < threshold]

def main():
    """Run the program."""
    stock_data = load_data()
    logs = []
    stock_data, logs = add_item(stock_data, "apple", 10, logs)
    stock_data, logs = add_item(stock_data, "banana", -2, logs)
    stock_data, logs = add_item(stock_data, "mango", 5, logs)
    stock_data = remove_item(stock_data, "apple", 3)
    stock_data = remove_item(stock_data, "orange", 1)
    print(f"Apple stock: {get_qty(stock_data, 'apple')}")
    print(f"Low items: {check_low_items(stock_data)}")
    save_data(data=stock_data)
    print_data(stock_data)
    logging.info("Program finished successfully.")

if __name__ == "__main__":
    main()
