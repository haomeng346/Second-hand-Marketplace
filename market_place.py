"""
Second-hand Marketplace
author: Haomeng DU, also Hugh Declan
"""

from typing import Dict, List, Tuple, Optional, Callable
import csv
import os
import random

# ------------------------ Constants ------------------------

# four csv file to mimic the database, use to store the data
# XXXX_CSV use to indicate the path of four data directory
DATA_DIR = "data"
USERS_CSV = os.path.join(DATA_DIR, "users.csv")
ITEMS_CSV = os.path.join(DATA_DIR, "items.csv")
LISTINGS_CSV = os.path.join(DATA_DIR, "listings.csv")
ORDERS_CSV = os.path.join(DATA_DIR, "orders.csv")

# eight categories to use check and search(by category)
CATEGORIES = [
    "Electronics",
    "Books",
    "Furniture",
    "Fashion",
    "Sports",
    "Home",
    "Toys",
    "Others"
]
# five conditions use to give the price recommendation
CONDITIONS = [
    "NEW",
    "LIKE_NEW",
    "VERY_GOOD",
    "GOOD",
    "ACCEPTABLE"
]
# different categories have different baseline to give the price recommendation
CATEGORY_BASELINE = {
    "Electronics": 300.0,
    "Books": 20.0,
    "Furniture": 150.0,
    "Fashion": 50.0,
    "Sports": 80.0,
    "Home": 60.0,
    "Toys": 25.0,
    "Others": 40.0,
}
# five conditions of item to give the price recommendation
CONDITION_MULTIPLIER = {
    "NEW": 1.00,
    "LIKE_NEW": 0.90,
    "VERY_GOOD": 0.80,
    "GOOD": 0.65,
    "ACCEPTABLE": 0.50,
}
# use this set to store the str used to get back from function
BACK_TOKENS = {
    "cd .."
}

# ------------------------ Tools ------------------------

# define functions to as tools to reduce the redundancy of code
'''
ensure_dirs(): to ensure the existence of a data directoru
ensure_csv(): to ensure the existence of csv files
title_case(): to reformat the str into capitalisation
parse_bool(): to parse the input (like "true", "1", "yes", "y") into boolean (True of False)
bool_str(): to change the boolean True or False to string "True" or "False"
generate_id(): to generate a unique id for users, listings, orders, and so on
is_back(): to check if a user is wanna go back
prompt_loop_back(): envelop the input into standard value or None
prompt_text(): to prompt the user to input a string
prompt_float(): to prompt the user to input a float
prompt_int(): to prompt the user to input a integer
'''

# to ensure the existence of a data directory
def ensure_dirs() -> None:
    """
    Ensure data directory exists.
    """
    os.makedirs(DATA_DIR, exist_ok=True)

# to ensure the existence of CSV files,
# in other words, to ensure the validation of CSV file path
def ensure_csv(path: str, headers: List[str]) -> None:
    """
    Ensure CSV exists with given headers; if missing, create with header.
    If the header does not exist, create a header for the CSV file.
    """
    if not os.path.exists(path):
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()

# to reformat the str into capitalisation
def title_case(string: str) -> str:
    """
    Normalise to capitalisation for storage or display.
    """
    return " ".join(word.capitalize() for word in string.strip().split())

# to parse the input (like "true", "1", "yes", "y") into boolean (True of False)
def parse_bool(string: str) -> bool:
    """
    Parse the input (like "true", "1", "yes", "y") into boolean (True of False).
    """
    return str(string).strip().lower() in ("true", "1", "yes", "y")

# to change the boolean True or False to string "True" or "False"
def bool_str(boolean: bool) -> str:
    """
    Convert the boolean type into string type.
    """
    return "True" if boolean else "False"

# to generate a unique id for users, listings, orders, and so on
def generate_id(existing: Dict[str, object]) -> str:
    """
    Generate a 6-digit numeric ID unique within a table.
    """
    while True:
        value = str(random.randint(100000, 999999))
        if value not in existing:
            return value

# to check if a user is wanna go back,
# i.e. input the str "cd .." to indicate back
def is_back(s: str) -> bool:
    """
    Check if input string means 'go back' (supports cd ..).
    """
    return s.strip().lower() in BACK_TOKENS

# envelop the input into standard value or None
def prompt_loop_back(
        prompt_hint: str,
        validator: Callable[[str], Optional[str]]
) -> Optional[str]:
    """
    Prompt with validation.
    Type 'cd ..' to go back.
    """
    while True:
        string = input(f"{prompt_hint} (type 'cd ..' to go back): ").strip()
        if is_back(string):
            return None
        norm = validator(string)
        if norm is not None:
            return norm

# to prompt the user to input a string
def prompt_text(
        label: str,
        allow_empty: bool = False
) -> Optional[str]:
    """
    Prompt text input.
    Type 'cd ..' to cancel or return.
    """
    while True:
        string = input(f"{label} (type 'cd ..' to go back): ").strip()
        if is_back(string):
            return None
        if string or allow_empty:
            return string
        print("Input cannot be empty.")

# to prompt the user to input a float, if enter the "Enter", then accept the defualt value
def prompt_float(
        label: str,
        default_val: Optional[float] = None,
        min_val: Optional[float] = None
) -> Optional[float]:
    """
    Prompt float input.
    Type 'cd ..' to cancel or return.

    Parameters:
        label: str type, the hint
        default_val: float type, oprional, default value to return if input is empty.
        min_val: float type, optional,
            if designated, then it would be the minimum value to return if input is greater than to this value.
    """
    while True:
        disp = f" [default {default_val:.2f}]" \
            if default_val is not None else ""
        string = input(f"{label}{disp} (Enter=accept, 'cd ..'=back): ").strip()
        if is_back(string):
            return None
        if string == "" and default_val is not None:
            return float(default_val)
        try:
            x = float(string)
            if min_val is not None and x < min_val:
                print(f"Value must be >= {min_val}")
                continue
            return x
        except ValueError:
            print("Please enter a valid number.")

# to prompt the user to input an integer
def prompt_int(
        label: str,
        min_val: Optional[int] = None,
        max_val: Optional[int] = None
) -> Optional[int]:
    """
    Prompt integer input.
    Type 'cd ..' to cancel or return.
    """
    while True:
        string = input(f"{label} ('cd ..' to go back): ").strip()
        if is_back(string):
            return None
        try:
            x = int(string)
            if min_val is not None and x < min_val:
                print(f"Value must be >= {min_val}")
                continue
            if max_val is not None and x > max_val:
                print(f"Value must be <= {max_val}")
                continue
            return x
        except ValueError:
            print("Please enter a valid integer.")

# ------------------------ Entities ------------------------

class User:
    """
    User entity.
    """
    def __init__(
            self,
            user_id: str,
            username: str,
            password: str
    ):
        self.id = user_id
        self.username = username
        self.password = password

    # convert value of class User's attributes
    # into a dictionary for write to CSV file
    def to_row(self) -> dict:
        return {
            "user_id": self.id,
            "username": self.username,
            "password": self.password,
        }

# get the users.csv table attributes list
def user_headers() -> List[str]:
    return [
        "user_id",
        "username",
        "password"
    ]

# get a record from users.csv as a dictionary
def user_from_row(row: dict) -> User:
    return User(
        user_id= row["user_id"],
        username = row["username"],
        password = row["password"]
    )

class Item:
    """
    Item entity.
    """
    def __init__(
            self,
            item_id: str,
            name: str,
            category: str,
            brand: str,
            condition: str,
            description: str
    ):
        self.id = item_id
        self.name = name
        self.category = category
        self.brand = brand
        self.condition = condition
        self.description = description

    def to_row(self) -> dict:
        return {
            "item_id": self.id,
            "name": self.name,
            "category": self.category,
            "brand": self.brand,
            "condition": self.condition,
            "description": self.description
        }

def item_headers() -> List[str]:
    return [
        "item_id",
        "name",
        "category",
        "brand",
        "condition",
        "description"
    ]

def item_from_row(row: dict) -> Item:
    return Item(
        item_id= row["item_id"],
        name = row["name"],
        category = row["category"],
        brand = row["brand"],
        condition = row["condition"],
        description = row["description"],
    )

class Listing:
    """
    Listing entity.
    """
    def __init__(
            self,
            listing_id: str,
            item_id: str,
            seller_id: str,
            price: float,
            quantity: int,
            active: bool,
            deleted: bool
    ):
        self.id = listing_id
        self.item_id = item_id
        self.seller_id = seller_id
        self.price = float(price)
        self.quantity = int(quantity)
        self.active = bool(active)
        self.deleted = bool(deleted)

    def to_row(self) -> dict:
        return {
            "listing_id": self.id,
            "item_id": self.item_id,
            "seller_id": self.seller_id,
            "price": f"{self.price:.2f}",
            "quantity": str(self.quantity),
            "active": bool_str(self.active),
            "deleted": bool_str(self.deleted),
        }

def listing_headers() -> List[str]:
    return [
        "listing_id",
        "item_id",
        "seller_id",
        "price",
        "quantity",
        "active",
        "deleted"
    ]

def listing_from_row(row: dict) -> Listing:
    return Listing(
        listing_id= row["listing_id"],
        item_id = row["item_id"],
        seller_id = row["seller_id"],
        # row.get("price", "0") will return the value of key="price" in dictionary row
        # if the key "price" donot exist, then return "0"
        # if the value of key="price" is '' or None, row.get() will return it
        # in this case, row.get("price", "0") or 0 will return 0
        price = float(row.get("price", "0") or 0),
        quantity = int(row.get("quantity", "0") or 0),
        active = parse_bool(row.get("active", "True")),
        deleted = parse_bool(row.get("deleted", "False")),
    )

class Order:
    """
    Order entity.
    """
    def __init__(
            self,
            order_id: str,
            buyer_id: str,
            seller_id: str,
            listing_id: str,
            unit_price: float,
            quantity: int,
            total_price: float,
            status: str
    ):
        self.id = order_id
        self.buyer_id = buyer_id
        self.seller_id = seller_id
        self.listing_id = listing_id
        self.unit_price = float(unit_price)
        self.quantity = int(quantity)
        self.total_price = float(total_price)
        self.status = status

    def to_row(self) -> dict:
        return {
            "order_id": self.id,
            "buyer_id": self.buyer_id,
            "seller_id": self.seller_id,
            "listing_id": self.listing_id,
            "unit_price": f"{self.unit_price:.2f}",
            "quantity": str(self.quantity),
            "total_price": f"{self.total_price:.2f}",
            "status": self.status
        }

def order_headers() -> List[str]:
    return [
        "order_id",
        "buyer_id",
        "seller_id",
        "listing_id",
        "unit_price",
        "quantity",
        "total_price",
        "status"
    ]

def order_from_row(row: dict) -> Order:
    return Order(
        order_id= row["order_id"],
        buyer_id = row["buyer_id"],
        seller_id = row["seller_id"],
        listing_id = row["listing_id"],
        unit_price = float(row.get("unit_price", "0") or 0),
        quantity = int(row.get("quantity", "0") or 0),
        total_price = float(row.get("total_price", "0") or 0),
        status = row.get("status", "COMPLETED")
    )

# ------------------------ Controller ------------------------

class Marketplace:
    """
    Marketplace manager: initialisation, operations, CSV I/O, autosave.
    """
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.items: Dict[str, Item] = {}
        self.listings: Dict[str, Listing] = {}
        self.orders: Dict[str, Order] = {}

    # ----- CSV I/O -----
    def _load_csv(
            self,
            path: str,
            headers: List[str],
            dst: Dict[str, object],
            from_row_func: Callable[[dict], object],
            id_key: str
    ):
        ensure_csv(path, headers)
        dst.clear()
        with open(path, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # skip the empty row
                if not row.get(id_key):
                    continue
                obj = from_row_func(row)
                dst[row[id_key]] = obj

    def _save_csv(
            self,
            path: str,
            headers: List[str],
            source: Dict[str, object]
    ):
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            for one_object in source.values():
                writer.writerow(one_object.to_row())

    def load_all_csv(self) -> None:
        """
        Load all tables from CSV.
        """
        ensure_dirs()
        self._load_csv(
            USERS_CSV,
            user_headers(),
            self.users,
            user_from_row,
            "user_id"
        )
        self._load_csv(
            ITEMS_CSV,
            item_headers(),
            self.items,
            item_from_row,
            "item_id"
        )
        self._load_csv(
            LISTINGS_CSV,
            listing_headers(),
            self.listings,
            listing_from_row,
            "listing_id"
        )
        self._load_csv(
            ORDERS_CSV,
            order_headers(),
            self.orders,
            order_from_row,
            "order_id"
        )

    def save_all_csv(self) -> None:
        """
        Save all tables to CSV with current headers.
        """
        ensure_dirs()
        self._save_csv(
            USERS_CSV,
            user_headers(),
            self.users
        )
        self._save_csv(
            ITEMS_CSV,
            item_headers(),
            self.items
        )
        self._save_csv(
            LISTINGS_CSV,
            listing_headers(),
            self.listings
        )
        self._save_csv(
            ORDERS_CSV,
            order_headers(),
            self.orders
        )



    # ----- Operations -----

    def register(
            self,
            username: str,
            password: str
    ) -> User:
        """
        Register a new user.
        Autosave.
        """
        user_name = title_case(username)
        if not user_name or not password:
            raise ValueError("Username and password cannot be empty.")
        if any(
                u.username.lower() == user_name.lower()
                for u in self.users.values()
        ):
            raise ValueError("Username already exists.")
        user_id = generate_id(self.users)
        user = User(user_id= user_id, username = user_name, password = password)
        self.users[user.id] = user
        self.save_all_csv()
        return user

    def login(
            self,
            username: str,
            password: str
    ) -> Optional[User]:
        """
        Login by username and password.
        """
        uname = title_case(username)
        for user in self.users.values():
            if user.username == uname and user.password == password:
                return user
        return None

    def post_listing(
            self,
            seller: User,
            name: str,
            category: str,
            brand: str,
            condition: str,
            description: str,
            price: float,
            quantity: int
    ) -> Listing:
        """
        Post a new listing.
        Creates Item and Listing.
        Autosave.
        """
        category = title_case(category)
        cond_up = condition.strip().upper()
        if category not in CATEGORIES:
            raise ValueError("Unknown category.")
        if cond_up not in CONDITIONS:
            raise ValueError("Unknown condition.")
        if price <= 0 or quantity <= 0:
            raise ValueError("Price and quantity must be positive.")

        item_id = generate_id(self.items)
        item = Item(
            item_id= item_id,
            name = title_case(name),
            category = category,
            brand = title_case(brand),
            condition = cond_up,
            description = title_case(description)
        )
        self.items[item.id] = item

        listing_id = generate_id(self.listings)
        listing = Listing(
            listing_id= listing_id,
            item_id = item.id,
            seller_id = seller.id,
            price = round(float(price), 2),
            quantity = int(quantity),
            active = True,
            deleted = False
        )
        self.listings[listing.id] = listing
        self.save_all_csv()
        return listing

    def delete_listing(
            self,
            seller: User,
            listing_id: str
    ) -> None:
        """
        Soft delete a listing.
        Mark deleted = True and active = False.
        Autosave.
        """
        if listing_id not in self.listings:
            raise ValueError("Listing not found.")
        listing = self.listings[listing_id]
        if listing.seller_id != seller.id:
            raise ValueError("You can only delete your own listings.")
        listing.deleted = True
        listing.active = False
        self.save_all_csv()

    def search_by_category(self, category: str) -> List[Listing]:
        """
        Search active listings by category.
        Exclude deleted listings.
        """
        category = title_case(category)
        return [
            listing
            for listing in self.listings.values()
            if (
                    not listing.deleted
                    and listing.active
                    and listing.quantity > 0
                    and self.items[listing.item_id].category == category
            )
        ]

    def search_by_full_name(self, full_name: str) -> List[Listing]:
        """
        Search active listings by exact full name.
        Exclude deleted listings.
        """
        target = title_case(full_name)
        return [
            listing
            for listing in self.listings.values()
            if (
                    not listing.deleted
                    and listing.active
                    and listing.quantity > 0
                    and self.items[listing.item_id].name == target
            )
        ]

    def price_suggestion(
            self,
            category: str,
            condition: str
    ) -> Tuple[float, float, float]:
        """
        Price suggestion: suggestion_price = category baseline × condition multiplier.
        return: tuple(suggestion_price, suggestion_price * 0.9, suggestion_price * 1.1)
        """
        category = title_case(category)
        baseline = CATEGORY_BASELINE.get(
            category,
            CATEGORY_BASELINE["Others"]
        )
        multiplier = CONDITION_MULTIPLIER.get(
            condition.strip().upper(),
            0.65
        )
        suggestion_price = round(baseline * multiplier, 2)
        return (
            suggestion_price,
            round(suggestion_price * 0.9, 2),
            round(suggestion_price * 1.1, 2)
        )

    def buy_listing(
            self,
            buyer: User,
            listing_id: str,
            quantity: int
    ) -> Order:
        """
        Create an order and decrease stock.
        Autosave.
        """
        if listing_id not in self.listings:
            raise ValueError("Listing not found.")
        listing = self.listings[listing_id]
        if (
                listing.deleted
                or (not listing.active)
                or listing.quantity <= 0
        ):
            raise ValueError("Listing not available.")
        if quantity <= 0 or quantity > listing.quantity:
            raise ValueError("Invalid quantity.")
        order_id = generate_id(self.orders)
        order = Order(
            order_id= order_id,
            buyer_id = buyer.id,
            seller_id = listing.seller_id,
            listing_id = listing.id,
            unit_price = listing.price,
            quantity = quantity,
            total_price = round(listing.price * quantity, 2),
            status = "COMPLETED"
        )
        self.orders[order.id] = order
        listing.quantity -= quantity
        if listing.quantity <= 0:
            listing.active = False
        self.save_all_csv()
        return order

# ------------------------ Client ------------------------

def print_main_menu():
    """
    Print the main menu.
    """
    print("\n=== Second-hand Marketplace ===")
    print("1) Register")
    print("2) Login")
    print("3) View all active listings")
    print("4) Search by category")
    print("5) Search by full name")
    print("0) Quit")

def print_user_menu(user_name: str):
    """
    Print the user menu.
    """
    print(f"\n=== Welcome, {user_name} ===")
    print("1) Post a new listing")
    print("2) All my listings")
    print("3) Buy a listing")
    print("4) Delete my listing")
    print("5) View all active listings")
    print("6) My orders (as buyer)")
    print("7) Orders for my listings (as seller)")
    print("0) Logout")

def show_listing(market_place: Marketplace, listing: Listing):
    """
    Print one listing.
    """
    item = market_place.items[listing.item_id]
    seller = market_place.users.get(listing.seller_id)
    seller_name = seller.username if seller else "unknown"
    print(
        f"- ID: {listing.id} | Name: {item.name} | "
        f"Brand: {item.brand} | [{item.category}] ({item.condition}) | "
        f"${listing.price:.2f} x{listing.quantity} | seller: {seller_name}"
    )

def listing_status(listing: Listing) -> str:
    """
    Return status of listing according to its status(deleted, quantity, active).
    """
    if listing.deleted:
        return "DELETED"
    if listing.quantity <= 0:
        return "SOLD_OUT"
    if not listing.active:
        return "INACTIVE"
    return "ACTIVE"

def show_listing_with_status(
        market_place: Marketplace,
        listing: Listing
):
    """
    Print one listing with its status.
    """
    item = market_place.items[listing.item_id]
    status = listing_status(listing)
    seller_name = market_place.users.get(listing.seller_id).username \
        if listing.seller_id in market_place.users else "unknown"
    print(
        f"- ID: {listing.id} | Status: {status} | "
        f"Name: {item.name} | Brand: {item.brand} | "
        f"[{item.category}] ({item.condition}) | "
        f"${listing.price:.2f} x{listing.quantity} | seller: {seller_name}"
    )

def list_active_listings(market_place: Marketplace) -> List[Listing]:
    """
    Print and return all active, non-deleted listings.
    """
    active = [
        listing for listing in market_place.listings.values()
        if not listing.deleted
           and listing.active
           and listing.quantity > 0
    ]
    if not active:
        print("No active listings.")
    else:
        print(f"{len(active)} active listing(s):")
        for lis in active:
            show_listing(market_place, lis)
    return active

def validate_category_input(category: str) -> Optional[str]:
    """
    Validate category (case-insensitive).
    Return capitalised category if valid.
    """
    cate = title_case(category)
    if cate in CATEGORIES:
        return cate
    print("Unknown category. Available categories are:")
    print(", ".join(CATEGORIES))
    return None

def validate_condition_input(condition: str) -> Optional[str]:
    """
    Validate condition (case-insensitive).
    Return upper case of condition if valid.
    """
    cond = condition.strip().upper()
    if cond in CONDITIONS:
        return cond
    print("Unknown condition. Choose from:", ", ".join(CONDITIONS))
    return None

def show_order(market_place: Marketplace, order: Order):
    """
    Print one order with item name and brand if available.
    """
    lis = market_place.listings.get(order.listing_id)
    it_name, it_brand = "(listing missing)", "-"
    if lis:
        it = market_place.items.get(lis.item_id)
        if it:
            it_name, it_brand = it.name, it.brand
    buyer = market_place.users.get(order.buyer_id).username \
        if order.buyer_id in market_place.users else "unknown"
    seller = market_place.users.get(order.seller_id).username \
        if order.seller_id in market_place.users else "unknown"
    print(f"- Order ID: {order.id} | Item: {it_name} | "
          f"Brand: {it_brand} | Qty: {order.quantity} | "
          f"Unit: ${order.unit_price:.2f} | Total: ${order.total_price:.2f} | "
          f"Buyer: {buyer} | Seller: {seller} | Status: {order.status}"
    )

def list_my_purchased_orders(market_place: Marketplace, user: User):
    """
    List the orders that I bought.
    """
    my_orders = [
        order for order in market_place.orders.values()
        if order.buyer_id == user.id
    ]
    if not my_orders:
        print("You have no orders as buyer.")
        return
    print(f"You have {len(my_orders)} order(s) as buyer:")
    for order in my_orders:
        show_order(market_place, order)

def list_my_sold_orders(market_place: Marketplace, user: User):
    """
    List the orders that I sold.
    """
    my_orders = [
        order for order in market_place.orders.values()
        if order.seller_id == user.id
    ]
    if not my_orders:
        print("No orders for your listings yet.")
        return
    print(f"You have {len(my_orders)} order(s) for your listings:")
    for order in my_orders:
        show_order(market_place, order)

# ------------------------ Main loop ------------------------

def main():
    ensure_dirs()
    market_place = Marketplace()
    market_place.load_all_csv()

    current_user: Optional[User] = None

    while True:
        if not current_user:
            print_main_menu()
            command = input("Choose: ").strip()
            if command == "1":
                user_name = prompt_text(
                    "Username (Capitalisation format will be stored): "
                )
                if user_name is None:
                    continue
                password = prompt_text("Password: ")
                if password is None:
                    continue
                try:
                    user = market_place.register(user_name, password)
                    print(f"Registered: {user.username} (User ID: {user.id})")
                except ValueError as e:
                    print(f"Error: {e}")

            elif command == "2":
                user_name = prompt_text("Username: ")
                if user_name is None:
                    continue
                password = prompt_text("Password: ")
                if password is None:
                    continue
                user = market_place.login(user_name, password)
                if user:
                    current_user = user
                    print(f"Logged in as {user.username}")
                else:
                    print("Unmatched username and password.")

            elif command == "3":
                list_active_listings(market_place)

            elif command == "4":
                print("Available categories:", ", ".join(CATEGORIES))
                category = prompt_loop_back(
                    "Category", validate_category_input
                )
                if category is None:
                    continue
                results = market_place.search_by_category(category)
                if not results:
                    print("No listings in this category.")
                else:
                    print(f"Found {len(results)} listing(s):")
                    for listing in results:
                        show_listing(market_place, listing)

            elif command == "5":
                full_name = prompt_text("Full item item_name (exactly): ")
                if full_name is None:
                    continue
                results = market_place.search_by_full_name(full_name)
                if not results:
                    print(f"No listings of {full_name} found.")
                else:
                    print(f"Found {len(results)} listing(s):")
                    for listing in results:
                        show_listing(market_place, listing)

            elif command == "0":
                print("Goodbye ~\nSee you later!.")
                break
            else:
                print("Invalid command.")

        else:
            print_user_menu(current_user.username)
            command = input("Choose: ").strip()

            if command == "1":
                # Add a listing
                category = prompt_loop_back(
                    f"Category {CATEGORIES}", validate_category_input
                )
                if category is None:
                    continue
                item_name = prompt_text("Item item_name (full): ")
                if item_name is None:
                    continue
                condition = prompt_loop_back(
                    f"Condition {CONDITIONS}", validate_condition_input
                )
                if condition is None:
                    continue
                brand = prompt_text("Brand: ")
                if brand is None:
                    continue
                description = prompt_text(
                    "Description (optional, can be empty): ", allow_empty=True
                )
                if description is None:
                    continue
                suggest_price, low, high = market_place.price_suggestion(
                    category,
                    condition
                )
                print(
                    f"Suggested price: ${suggest_price:.2f} "
                    f"(range ${low:.2f} - ${high:.2f})"
                )
                price = prompt_float(
                    "Price",
                    default_val=suggest_price,
                    min_val=0.01
                )
                if price is None:
                    continue
                quantity = prompt_int("Quantity", min_val=1)
                if quantity is None:
                    continue
                try:
                    listing = market_place.post_listing(
                        current_user,
                        item_name,
                        category,
                        brand,
                        condition,
                        description,
                        price, quantity
                    )
                    print(f'''Posted listing {listing.id} for {title_case(item_name)} 
                    at ${listing.price:.2f} x{listing.quantity}''')
                except ValueError as e:
                    print(f"Error: {e}")

            elif command == "2":
                # All my listings (including deleted or sold out)
                mine_all = [
                    listing for listing in market_place.listings.values()
                    if listing.seller_id == current_user.id
                ]
                if not mine_all:
                    print("You have no listings yet.")
                else:
                    print(f"All your listings ({len(mine_all)}):")
                    for listing in mine_all:
                        show_listing_with_status(market_place, listing)

            elif command == "3":
                # Buy a listing
                available = list_active_listings(market_place)
                if not available:
                    continue
                listing_id = prompt_text("Enter Listing ID to buy")
                if listing_id is None:
                    continue
                quantity = prompt_int("Quantity", min_val=1)
                if quantity is None:
                    continue
                try:
                    order = market_place.buy_listing(
                        current_user,
                        listing_id,
                        quantity
                    )
                    print(f'''Order {order.id} created: ${order.total_price:.2f} 
                    for {quantity} unit(s). \nArrange offline payment/delivery.''')
                except ValueError as e:
                    print(f"Error: {e}")

            elif command == "4":
                # Delete my listing
                candidates = [
                    listing for listing in market_place.listings.values()
                    if listing.seller_id == current_user.id
                       and not listing.deleted and listing.active
                ]
                if not candidates:
                    print("You have no active listings to delete.")
                    continue
                print("Your active listings:")
                for listing in candidates:
                    show_listing(market_place, listing)
                listing_id = prompt_text("Listing ID to delete")
                if listing_id is None:
                    continue
                try:
                    market_place.delete_listing(current_user, listing_id)
                    print("Listing deleted (soft).")
                except ValueError as e:
                    print(f"Error: {e}")

            elif command == "5":
                list_active_listings(market_place)

            elif command == "6":
                list_my_purchased_orders(market_place, current_user)

            elif command == "7":
                list_my_sold_orders(market_place, current_user)

            elif command == "0":
                current_user = None
                print("Logged out.")
            else:
                print("Invalid command.")

if __name__ == "__main__":
    main()
