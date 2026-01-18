import mysql.connector

# connect to MySQL
con = mysql.connector.connect(
    host="localhost",
    user="root",
    database="test"
)

cursor = con.cursor()

SHOPKEEPER_PASSWORD = "1234"

# -----------------------------
# SHOPKEEPER FUNCTIONS
# -----------------------------
def add_product():
    name = input("Enter product name: ")
    price = float(input("Enter price: "))
    qty = int(input("Enter quantity: "))
    cursor.execute("INSERT INTO products (pname, price, quantity) VALUES (%s, %s, %s)", (name, price, qty))
    con.commit()
    print("Product added successfully!\n")

def view_products():
    cursor.execute("SELECT * FROM products")
    data = cursor.fetchall()
    print("\n--- PRODUCT LIST ---")
    for row in data:
        print(f"ID: {row[0]} | Name: {row[1]} | Price: {row[2]} | Stock: {row[3]}")
    print()

def view_sales():
    cursor.execute("SELECT pname, quantity FROM sales")
    data = cursor.fetchall()

    print("\n--- SOLD ITEMS ---")
    if len(data) == 0:
        print("No items sold yet.\n")
        return

    for pname, qty in data:
        print(f"Item Sold: {pname} | Quantity: {qty}")
    print()

# -----------------------------
# CUSTOMER PURCHASE
# -----------------------------
def customer_purchase():
    cursor.execute("SELECT pid, pname, price, quantity FROM products")
    items = cursor.fetchall()

    print("\n--- AVAILABLE PRODUCTS ---")
    for row in items:
        print(f"ID: {row[0]} | {row[1]} | Price: ₹{row[2]} | Stock: {row[3]}")

    pid = int(input("Enter product ID to purchase: "))
    qty = int(input("Enter quantity: "))

    cursor.execute("SELECT pname, price, quantity FROM products WHERE pid=%s", (pid,))
    result = cursor.fetchone()

    if result is None:
        print("Invalid Product!\n")
        return

    pname, price, stock = result

    if qty > stock:
        print("Not enough stock!\n")
        return

    # Update stock
    cursor.execute("UPDATE products SET quantity = quantity - %s WHERE pid=%s", (qty, pid))
    con.commit()

    # Record sale
    cursor.execute("INSERT INTO sales (pname, quantity) VALUES (%s, %s)", (pname, qty))
    con.commit()

    print("\n--- BILL ---")
    print(f"Item: {pname}")
    print(f"Price: ₹{price}")
    print(f"Quantity: {qty}")
    print(f"Total: ₹{price * qty}")
    print("Purchase successful!\n")

# -----------------------------
# SHOPKEEPER MENU
# -----------------------------
def shopkeeper_menu():
    while True:
        print("\n===== SHOPKEEPER MENU =====")
        print("1. Add Product")
        print("2. View Products")
        print("3. View Sales Record")
        print("4. Exit")

        ch = input("Enter choice: ")

        if ch == "1":
            add_product()
        elif ch == "2":
            view_products()
        elif ch == "3":
            view_sales()
        elif ch == "4":
            print("Returning to main menu...\n")
            break
        else:
            print("Invalid choice.\n")

# -----------------------------
# MAIN PROGRAM
# -----------------------------
def main():
    while True:
        print("\nAre you:")
        print("1. Customer")
        print("2. Shopkeeper")
        print("3. Exit")

        role = input("Enter choice: ")

        if role == "1":
            customer_purchase()

        elif role == "2":
            password = input("Enter shopkeeper password: ")
            if password == SHOPKEEPER_PASSWORD:
                shopkeeper_menu()
            else:
                print("Incorrect password!\n")

        elif role == "3":
            print("Thank you for using Bakery Management System!")
            break

        else:
            print("Invalid choice.\n")

main()