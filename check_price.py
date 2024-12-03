from database import get_database_session
from data_model import Product

def check_price():
    db_session = get_database_session()
    products = db_session.query(Product).all()


    while True:
        print("\nProducts being tracked:")
        
        # Display the menu dynamically
        for i, option in enumerate(products, start=1):
            print(f"{i}. {option.name}")

        try:
            # Get user input and convert it to an integer
            choice = int(input("Enter your choice [number]: "))

            if choice < 1 or choice > len(products):
                print("Invalid choice! Please select a valid option.")
                continue
            print(products[choice-1].name)
            quit()
        except ValueError:
            print("Invalid input! Please enter a number.")




if __name__ == "__main__":
    check_price()