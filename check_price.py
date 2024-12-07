from database import get_database_session
from data_model import Product, ProductPlatform

def check_price():
    db_session = get_database_session()
    products = db_session.query(Product).all()

    products_name = [product.name for product in products]
    product_choice = get_user_input("Products being tracked", products_name)
    product = products[product_choice]

    product_platforms = db_session.query(ProductPlatform).filter(ProductPlatform.product_id==product.id).all()
    platforms_name = [platform.platform.name for platform in product_platforms]
    platforms_name.append("All Platforms")
    platform_choice = get_user_input(f"I want to check {product.name} on the following platform:", platforms_name)
    
    

def get_user_input(header_message, options):
    while True:
        print(f"\n{header_message}:")

        # Display the menu dynamically
        for i, option in enumerate(options, start=1):
            print(f"{i}. {option}")

        try:
            choice = int(input("Enter your choice [number]: "))
            if choice < 1 or choice > len(options):
                print("Invalid choice! Please select a valid option.")
                continue
            # -1 to account for lists in python starting at 0
            return choice-1
        except ValueError:
            print("Invalid input! Please enter a number.")

    

if __name__ == "__main__":
    check_price()