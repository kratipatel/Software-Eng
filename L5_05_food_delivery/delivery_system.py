"""Food delivery order queue manager."""
import itertools
import json
from datetime import datetime

ORDERS = {}
MENU = {}
VALID_STATUSES = ["placed", "cooking", "out_for_delivery", "delivered"]
DEFAULT_MENU = {"pizza": 250, "burger": 150, "fries": 90, "coke": 40}
_ORDER_IDS = itertools.count(1)


def create_order(customer, items, order_history=None):
    """Create an order and return its id."""
    if not customer or not items:
        raise ValueError("Order needs a customer and at least one item")
    unknown = [i for i in items if i not in MENU]
    if unknown:
        raise ValueError(f"Unknown menu items: {unknown}")
    if order_history is None:
        order_history = []
    order_id = next(_ORDER_IDS)
    ORDERS[order_id] = {
        "customer": customer,
        "items": items,
        "total": sum(MENU[i] for i in items),
        "status": "placed",
    }
    order_history.append(order_id)
    return order_id


def update_order_status(order_id, status):
    """Change an order's status, rejecting bad ids and statuses."""
    if status not in VALID_STATUSES:
        raise ValueError(f"Invalid status: {status}")
    if order_id not in ORDERS:
        raise KeyError(f"Order {order_id} not found")
    ORDERS[order_id]["status"] = status


def read_menu_config(file="menu.json"):
    """Load the menu from a JSON file, falling back to defaults."""
    MENU.clear()
    try:
        with open(file, encoding="utf-8") as menu_file:
            MENU.update(json.load(menu_file))
    except (OSError, json.JSONDecodeError):
        MENU.update(DEFAULT_MENU)


def daily_revenue():
    """Return the total of all delivered orders."""
    return sum(
        order["total"]
        for order in ORDERS.values()
        if order["status"] == "delivered"
    )


def backup_orders(file="orders.json"):
    """Save all orders to a JSON file."""
    with open(file, "w", encoding="utf-8") as backup_file:
        json.dump(ORDERS, backup_file)


def restore_orders(file="orders.json"):
    """Load orders from a JSON file, restoring integer ids."""
    with open(file, encoding="utf-8") as backup_file:
        data = json.load(backup_file)
    ORDERS.clear()
    ORDERS.update({int(k): v for k, v in data.items()})


def print_queue():
    """Print every order in the queue."""
    print(f"Order queue at {datetime.now()}")
    for order_id, order in ORDERS.items():
        print(order_id, order["customer"], order["status"], order["total"])


def main():
    """Run a demo of the order queue."""
    read_menu_config()
    first = create_order("Asha", ["pizza", "coke"])
    second = create_order("Ravi", ["burger", "pizza"])
    update_order_status(first, "delivered")
    for order_id, status in [(second, "teleported"), (42, "delivered")]:
        try:
            update_order_status(order_id, status)
        except (ValueError, KeyError) as err:
            print("Error:", err)
    print("Revenue today:", daily_revenue())
    backup_orders()
    restore_orders()
    print_queue()


if __name__ == "__main__":
    main()
