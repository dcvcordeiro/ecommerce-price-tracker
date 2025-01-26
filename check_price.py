from sqlalchemy import func

from database import get_database_session
from data_model import Product, ProductPlatform, PriceHistory

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
    
    if platform_choice == len(platforms_name)-1:
        # TODO: Add hook for option "ALL"
        pass
    else:
        product_platform = product_platforms[platform_choice]
        min_product_price = db_session.query(PriceHistory, func.min(PriceHistory.price)).filter(PriceHistory.product_platform_id==product_platform.id).all()
        min_product_price = min_product_price[0][0]
        max_product_price = db_session.query(PriceHistory, func.max(PriceHistory.price)).filter(PriceHistory.product_platform_id==product_platform.id).all()
        max_product_price = max_product_price[0][0]
        current_product_price = db_session.query(PriceHistory, func.max(PriceHistory.date_checked)).filter(PriceHistory.product_platform_id==product_platform.id).all()
        current_product_price = current_product_price[0][0]
        avg_product_price = db_session.query(PriceHistory, func.avg(PriceHistory.price)).filter(PriceHistory.product_platform_id==product_platform.id).all()
        avg_product_price = avg_product_price[0][1]
        
        percentage_diff = (current_product_price.price - avg_product_price) * 100 / avg_product_price
        higher_lower = f"{percentage_diff:.2f}% higher" if percentage_diff > 0 else f"{percentage_diff:.2f}% lower"
        higher_lower = "the same" if percentage_diff == 0 else higher_lower

        print(f"""\nOn {product_platform.platform.name} the {product_platform.product.name} had: 
        - The highest price of {max_product_price.price}€ on {max_product_price.date_checked}
        - The lowest price of {min_product_price.price}€ on {min_product_price.date_checked}""")

        print(f"""\nThe last time it was checked ({current_product_price.date_checked}), the price was {higher_lower} than the average ({avg_product_price}€)""")
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