import mysql.connector
from datetime import datetime

# -------------------------------
# CONNECT TO MYSQL DATABASE
# -------------------------------
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",   # change if needed
    database="bakery"
)

cursor = connection.cursor()

# -------------------------------
# FUNCTIONS
# -------------------------------

def add_item():
    name = input("Enter item name: ")
    category = input("Enter category (Cake/Bread/Pastry/etc): ")
    price = float(input("Enter price: "))
    stock = int(input("Enter stock quantity: "))

    query = "INSERT INTO Items (ItemName, Category, Price, Stock) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (name, category, price, stock))
    connection.commit()
    print("\nItem added successfully!\n")


def view_items():
    cursor.execute("SELECT * FROM Items")
    rows = cursor.fetchall()

    print("\n----- ITEM LIST -----")
    for row in rows:
        print(row)
    print("----------------------\n")


def update_stock():
    item_id = int(input("Enter Item ID to update stock: "))
    new_stock = int(input("Enter new stock value: "))

    query = "UPDATE Items SET Stock=%s WHERE ItemID=%s"
    cursor.execute(query, (new_stock, item_id))
    connection.commit()
    print("\nStock updated!\n")


def delete_item():
    item_id = int(input("Enter Item ID to delete: "))

    cursor.execute("DELETE FROM Items WHERE ItemID=%s", (item_id,))
    connection.commit()
    print("\nItem deleted successfully!\n")


def purchase_stock():
    item_id = int(input("Enter Item ID to purchase: "))
    qty = int(input("Enter quantity purchased: "))

    cursor.execute(
        "INSERT INTO Purchases (ItemID, Quantity) VALUES (%s, %s)",
        (item_id, qty)
    )
    cursor.execute(
        "UPDATE Items SET Stock = Stock + %s WHERE ItemID=%s",
        (qty, item_id)
    )

    connection.commit()
    print("\nStock added through purchase!\n")


def sell_item():
    item_id = int(input("Enter Item ID to sell: "))
    qty = int(input("Enter quantity sold: "))

    cursor.execute(
        "SELECT Price, Stock FROM Items WHERE ItemID=%s",
        (item_id,)
    )
    result = cursor.fetchone()

    if result is None:
        print("\nItem not found!\n")
        return

    price, stock = result

    if qty > stock:
        print("\nNot enough stock!\n")
        return

    total = qty * price

    cursor.execute(
        "INSERT INTO Sales (ItemID, Quantity, TotalAmount) VALUES (%s, %s, %s)",
        (item_id, qty, total)
    )
    cursor.execute(
        "UPDATE Items SET Stock = Stock - %s WHERE ItemID=%s",
        (qty, item_id)
    )

    connection.commit()
    print(f"\nSale recorded! Total = ₹{total}\n")


def view_purchase_history():
    cursor.execute("SELECT * FROM Purchases")
    rows = cursor.fetchall()

    print("\n----- PURCHASE HISTORY -----")
    for row in rows:
        print(row)
    print("----------------------------\n")


def view_sales_history():
    cursor.execute("SELECT * FROM Sales")
    rows = cursor.fetchall()

    print("\n----- SALES HISTORY -----")
    for row in rows:
        print(row)
    print("-------------------------\n")


def calculate_total_sales():
    cursor.execute("SELECT SUM(TotalAmount) FROM Sales")
    total = cursor.fetchone()[0]

    if total is None:
        total = 0

    print(f"\nTotal Sales Amount = ₹{total}\n")


# -------------------------------
# MAIN MENU
# -------------------------------

while True:
    print("\n========== BAKERY MANAGEMENT ==========")
    print("1. Add New Item")
    print("2. View All Items")
    print("3. Update Stock")
    print("4. Delete Item")
    print("5. Purchase Stock (Add)")
    print("6. Sell Item")
    print("7. View Purchase History")
    print("8. View Sales History")
    print("9. Calculate Total Sales")
    print("10. Exit")
    print("======================================")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_item()
    elif choice == "2":
        view_items()
    elif choice == "3":
        update_stock()
    elif choice == "4":
        delete_item()
    elif choice == "5":
        purchase_stock()
    elif choice == "6":
        sell_item()
    elif choice == "7":
        view_purchase_history()
    elif choice == "8":
        view_sales_history()
    elif choice == "9":
        calculate_total_sales()
    elif choice == "10":
        print("\nExiting program...")
        break
    else:
        print("\nInvalid Choice! Try Again.\n")