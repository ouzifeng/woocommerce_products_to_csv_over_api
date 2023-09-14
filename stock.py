import requests
import csv

def fetch_all_products():
    base_url = "https://thetackletavern.co.uk/wp-json/wc/v3/"
    product_url = base_url + "products"
    params = {
        "consumer_key": "ck_033584debafe468c9b441298a89c21a4d499cf3e",
        "consumer_secret": "cs_84b7b046fbeda0095b20f84e122c2dce2ca7a5d3",
        "per_page": 100,
        "page": 1
    }
    
    all_products = []
    batch_size = 10
    batch_counter = 0
    
    print("Fetching products...")
    
    while True:
        response = requests.get(product_url, params=params)
        products = response.json()
        
        # Check if there's no more products to fetch
        if not products:
            break

        for product in products:
            if product['type'] == 'simple':
                sku = product['sku']
                price = product['price']
                stock_quantity = product['stock_quantity']
                all_products.append(["The Tackle Tavern", "en", sku, price, stock_quantity])
            elif product['type'] == 'variable':
                # Fetch variations for this product
                variations_url = product_url + f"/{product['id']}/variations"
                variations = requests.get(variations_url, params=params).json()
                for variation in variations:
                    sku = variation['sku']
                    price = variation['price']
                    stock_quantity = variation['stock_quantity']
                    all_products.append(["The Tackle Tavern", "en", sku, price, stock_quantity])
        
            batch_counter += 1
            if batch_counter % batch_size == 0:
                print(f"Fetched {batch_counter} products...")
        
        # Prepare to fetch the next page
        params['page'] += 1

    print(f"Total products fetched: {len(all_products)}.")
    
    # Write to CSV
    print("Writing to CSV...")
    with open('woocommerce_products.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Vendor', 'Language', 'Product Code', 'Price', 'Quantity'])
        writer.writerows(all_products)
    
    print("CSV generation complete.")

# Call the function
fetch_all_products()
