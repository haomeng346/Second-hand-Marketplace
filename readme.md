

---

---

---

# Second-hand Marketplace (CLI) — README

A simple command-line marketplace to post, search, and buy second-hand items. Data is persisted in CSV files under the data directory.

## Features

- Register and login users
- Post new listings (auto-creates corresponding items)
- View/search active listings (by category or full name)
- Buy a listing (creates an order and reduces stock)
- Soft delete your own listings
- Autosave to CSV files
- Input helpers: default values, validation, and “cd ..” to go back

## Requirements

- Python 3.8+ (standard library only; no extra dependencies)

## Project Structure

- data/: stores all CSV files
  - users.csv
  - items.csv
  - listings.csv
  - orders.csv
- main script: run this file directly

Note:

- The program will create data/ and empty CSVs with headers automatically if missing.

## Installation

1. Save your Python file (this script) to a directory and then run it directly.

2. **However, if you want to have some pre-writen data for test, you should put the four csv files into the ./path/**

3. the four csv files stored inside the data directory in the same path with market_place.py

4. you may should copy the four files outside the directory scaffold, i.e. same with the path of directory scaffold

5. the structure should as below:

   --project(dir)

   ​	----market_place.py

   ​	----data(dir)

   ​			----scaffold(dir)

   ​			----users.csv

   ​			----items.csv

   ​			----listings.csv

   ​			----orders.csv

   ​				



## Usage Guide

### Main Menu

- Register
  - Create a new user. Username is stored in Title Case; password stored as plaintext.
  
- Login
  - Login with username and password (case-insensitive for username via Title Case).
  
- View all active listings
  - Shows non-deleted, active listings with quantity > 0.
  
- Search by category
  - Valid categories:
    - Electronics, Books, Furniture, Fashion, Sports, Home, Toys, Others
  
- Search by full name
  - Exact match (case-insensitive formatting via Title Case).
  
- Quit

Tip: In most prompts, type cd .. to cancel and go back.

​		**Just as a easter egg for learning how to use simple terminal commands.**

### User Menu (after login)

- Post a new listing
  - Flow:
    - Category (validated against the list above)
    - Item name (full name)
    - Condition (one of: NEW, LIKE_NEW, VERY_GOOD, GOOD, ACCEPTABLE)
    - Brand
    - Description (optional; empty allowed)
    - Suggested price is shown based on category and condition. Press Enter to accept the default or enter your own price. Quantity must be a positive integer.
  - This creates both an Item and a Listing.
  
- All my listings
  - Show all your listings including DELETED, SOLD_OUT, INACTIVE, and ACTIVE.
  
- Buy a listing
  - Pick a listing ID from currently active ones, enter the quantity, and create an order. Stock is reduced; listing becomes inactive if stock reaches 0.
  
- Delete my listing
  - Soft delete (deleted=True, active=False) only for your own active listings.
  
- View all active listings

- My orders (as buyer)

- Orders for my listings (as seller)

- Logout

### Input Helpers and Conventions

- cd ..: At most prompts, enter cd .. to go back (cancel).
- Defaults: For price input, pressing Enter accepts the suggested default.
- Title Case: Usernames, item names, category, brand, and description are normalized to Title Case for consistency.
- Condition: Always uppercased and validated.
- Booleans: Stored as "True"/"False" strings in CSV.

## Data Persistence

CSV files are used as a lightweight database:

- users.csv: user profiles
- items.csv: item metadata
- listings.csv: sellable units (price, quantity, active/deleted flags)
- orders.csv: purchase history

The app autosaves on:

- Register, Post Listing, Delete Listing, Buy Listing

If you want to reset data, stop the program and delete files under data/ (the program will recreate them with just headers).

## CSV Headers

- users.csv
  - user_id, username, password
- items.csv
  - item_id, name, category, brand, condition, description
- listings.csv
  - listing_id, item_id, seller_id, price, quantity, active, deleted
- orders.csv
  - order_id, buyer_id, seller_id, listing_id, unit_price, quantity, total_price, status

## Pricing Suggestion

When posting a listing:

- The app shows a suggested price calculated as:
  - suggestion = CATEGORY_BASELINE[category] × CONDITION_MULTIPLIER[condition]
- If a category is not found, it falls back to CATEGORY_BASELINE["Others"].
- Returned range: suggestion, suggestion×0.9, suggestion×1.1

You can accept the default by pressing Enter or override it with your own price.

## Example Workflow

- Start the program: python your_script_name.py
- Register (1) → username: Alice → password: 123
- Login (2) with the same credentials
- Post a listing (User Menu → 1):
  - Category: Electronics
  - Item name: iPhone 12
  - Condition: LIKE_NEW
  - Brand: Apple
  - Description: Gently used
  - Suggested price appears; accept or override
  - Quantity: 1
- View all active listings (5) and note the listing ID
- Buy a listing (3) → enter listing ID and quantity
- View your orders as buyer (6)

## Troubleshooting

- CSV encoding: Files are opened with UTF-8; if you edit them manually, keep UTF-8.
- Windows newline: Files are opened with newline="" to avoid extra blank lines.
- “No active listings”: Make sure you created a listing and it’s active with quantity > 0.
- Category/Condition rejected: The app validates strictly; choose from the lists shown.
- Reset data: Delete files in data/ and re-run.

## License

COMP9001 Final project use only. 

## Author

Haomeng DU

also, Hugh Declan

