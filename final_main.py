import os
from inventory_item import InventoryItem

# Load inventory from the text file
def load_inventory(file_path):
    inventory = []
    with open(file_path, 'r') as file:
        for line in file:
            name, price, quantity = line.strip().split(',')
            item = InventoryItem(name, int(quantity), float(price))
            inventory.append(item)
    return inventory

# Save inventory to the text file
def save_inventory(file_path, inventory):
    with open(file_path, 'w') as file:
        for item in inventory:
            file.write(f"{item.get_product_name()},{item.get_product_price()},{item.get_product_quantity()}\n")

# Display the main menu
def display_main_menu():
    print("**********************************************************")
    print("*                                                        *")
    print("* 1. Vending Machine                                     *")
    print("* 2. Management                                          *")
    print("* 3. Quit                                                *")
    print("*                                                        *")
    print("**********************************************************")


def display_vending_menu(inventory):
    print("_________________________________________________________")
    print("|                                               |        |")
    print("|                *** Vending Machine ***        |PRICE $ |")
    print("|_______________________________________________|________|")
    print("|                                                        |")

    for idx, item in enumerate(inventory, start=1):
        name = item.get_product_name()
        price = item.get_product_price()
        
        # Calculate spaces needed for alignment
        idx_space = " " * (3 - len(str(idx)))
        name_space = " " * (42 - len(name))
        price_space = " " * (7 - len(str(price)))
        
        # Adjust the formatting for each item in the list
        print(f"| {idx}{idx_space}{name}  {name_space}{price_space}{price} |")

    print("|                                                        |")
    print("|________________________________________________________|")
    print()



# Handle the vending machine functionality
def vending_machine(inventory, file):
    return_to_main_menu = False
    while not return_to_main_menu:
        display_vending_menu(inventory)
        selection = int(input("Enter selection (1-10) or 0 to return to Main Menu: "))

        if selection == 0:
            return_to_main_menu = True
        elif 1 <= selection <= len(inventory):
            selected_item = inventory[selection - 1]
            confirm = input(f"You selected {selected_item.get_product_name()}. Is this correct (y/n)? ").lower()
            if confirm == 'y':
                process_transaction(selected_item, inventory, file)
        else:
            print("Invalid choice. Please try again.")

# Process the transaction (simplified version)
def process_transaction(item, inventory, file):
    print("Please continue to enter coins until amount reached.")
    print("Valid choices for coins are:")
    print("[1] Ten cents")
    print("[2] Twenty cents")
    print("[3] Fifty cents")
    print("[4] One dollar")
    print("[5] Two dollars")
    print("[6] Cancel")

    total_paid = 0
    coin_values = [0.10, 0.20, 0.50, 1.00, 2.00]

    transaction_completed = False
    while not transaction_completed:
        print(f"Balance: ${total_paid:.2f} Remaining: ${item.get_product_price() - total_paid:.2f}")
        coin_choice = int(input("Enter coin [1-5] or 6 to cancel: "))

        if coin_choice == 6:
            print(f"Transaction cancelled. Refund: ${total_paid:.2f}")
            return
        elif 1 <= coin_choice <= 5:
            total_paid += coin_values[coin_choice - 1]
            if total_paid >= item.get_product_price():
                transaction_completed = True
        else:
            print("Invalid choice. Please try again.")

    change = total_paid - item.get_product_price()
    print(f"Transaction completed. Refund: ${change:.2f}")
    item.reduce_product_quantity()
    save_inventory(file, inventory)




def management_menu(inventory):
    print("________________________________________________________________")
    print("|                                                               |")
    print("|                       *** INVENTORY ***                       |")
    print("|_______________________________________________________________|")
    print("| NO: | NAME                             |     PRICE | QUANTITY |")
    print("|'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''|")

    for idx, item in enumerate(inventory, start=1):
        name = item.get_product_name()
        price = item.get_product_price()
        quantity = item.get_product_quantity()

        # Calculate spaces needed for alignment
        idx_space = " " * (3 - len(str(idx)))
        name_space = " " * (32 - len(name))
        price_space = " " * (9 - len(str(price)))
        quantity_space = " " * (8 - len(str(quantity)))

        # Adjust the formatting for each item in the list
        print(f"| {idx}{idx_space} | {name}{name_space} |{price_space}{price}  |{quantity_space}{quantity}  |")

    print("|_______________________________________________________________|")
    print()



# Display the management menu
def display_management_menu(inventory, file):
    management_menu(inventory)

    manage_inventory = True
    while manage_inventory:
        print("*****************************************************************")
        print("*                                                               *")
        print("*   1. Update Quantity                                          *")
        print("*   2. Update Price                                             *")
        print("*   3. Return to main menu                                      *")
        print("*                                                               *")
        print("*****************************************************************")

        choice = int(input("Please enter 1-3 to select: "))

        if choice == 1:
            management_menu(inventory)
            update_quantity(inventory, file)
        elif choice == 2:
            management_menu(inventory)
            update_price(inventory, file)
        elif choice == 3:
            manage_inventory = False
        else:
            print("Please enter either 1, 2, or 3.")

# Update quantity of an item
def update_quantity(inventory, file):
    product_number = int(input("Enter product number from Inventory list: "))
    if 1 <= product_number <= len(inventory):
        selected_item = inventory[product_number - 1]
        confirm = input(f"You selected {selected_item.get_product_name()}. Is this correct (y/n)? ").lower()
        if confirm == 'y':
            new_quantity = int(input(f"Current quantity: {selected_item.get_product_quantity()} | Enter new quantity: "))
            selected_item.set_product_quantity(new_quantity)
            save_inventory(file, inventory)
            print(f"Updated quantity of {selected_item.get_product_name()} to {new_quantity}.")

        elif confirm =='n':
            display_management_menu(inventory, file)

    else:
        print("Invalid product number.")

# Update price of an item
def update_price(inventory, file):
    product_number = int(input("Enter product number from Inventory list: "))
    if 1 <= product_number <= len(inventory):
        selected_item = inventory[product_number - 1]
        confirm = input(f"You selected {selected_item.get_product_name()}. Is this correct (y/n)? ").lower()
        if confirm == 'y':
            new_price = float(input(f"Current price: ${selected_item.get_product_price():.2f} | Enter new price: "))
            selected_item.set_product_price(new_price)
            save_inventory(file, inventory)
            print(f"Updated price of {selected_item.get_product_name()} to ${new_price:.2f}.")
        
        elif confirm == 'n':
            display_management_menu(inventory, file)

    else:
        print("Invalid product number.")

# Main program
def main():
    inventory_file = 'inventory.txt'
    inventory = load_inventory(inventory_file)

    quit_program = False
    while not quit_program:
        display_main_menu()
        selection = int(input("Please enter 1-3 to select: "))

        if selection == 1:
            vending_machine(inventory, inventory_file)
        elif selection == 2:
            display_management_menu(inventory, inventory_file)
        elif selection == 3:
            confirm_exit = input("Are you sure (y/n)? ").lower()
            if confirm_exit == 'y':
                save_inventory(inventory_file, inventory)
                print("Writing inventory to file...")
                print("Terminating program... Goodbye.")
                quit_program = True
        else:
            print("Please enter either 1, 2, or 3.")

if __name__ == "__main__":
    main()
