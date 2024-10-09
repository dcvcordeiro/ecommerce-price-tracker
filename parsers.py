import requests
from bs4 import BeautifulSoup
import random

class Amazon():
    def get_price(url: str) -> float:
        return 0.0

import requests
from bs4 import BeautifulSoup

# URL of the product page
url = "https://www.fnac.pt/MacBook-Air-13-2024-M3-8-core-16GB-512GB-SSD-Cinzento-Sideral-Computador-Portatil-Macbook/a11808010"

# Headers to mimic a browser visit
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

# Sending a request to the webpage
response = requests.get(url, headers=headers)

# Checking if the request was successful
if response.status_code == 200:
    # Parsing the content of the webpage
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extracting the product price
    price = soup.find("div", {"class": "f-priceBox-price f-priceBox-price--reco"})
    if price:
        price = price.text.strip()
        print("Price:", price)
    else:
        print("Price element not found on the page.")
else:
    print("Failed to retrieve the webpage. Status code:", response.status_code)


"""
if __name__ == "__main__":
    fnac_parser = Fnac()
    url = "https://www.fnac.pt/MacBook-Air-13-2024-M3-8-core-16GB-512GB-SSD-Cinzento-Sideral-Computador-Portatil-Macbook/a11808010"
    price_product = fnac_parser.get_price(url)
    print(price_product)
"""