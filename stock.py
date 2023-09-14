import requests
import csv

def fetch_all_products():
    base_url = "ADD YOUR STORE URL/wp-json/wc/v3/"
    product_url = base_url + "products"
    params = {
        "consumer_key": "ADD API KEY",
        "consumer_secret": "ADD API SECRET",
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
                all_products.append([sku, price, stock_quantity])
            elif product['type'] == 'variable':
                # Fetch variations for this product
                variations_url = product_url + f"/{product['id']}/variations"
                variations = requests.get(variations_url, params=params).json()
                for variation in variations:
                    sku = variation['sku']
                    price = variation['price']
                    stock_quantity = variation['stock_quantity']
                    all_products.append([sku, price, stock_quantity])
        
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
        writer.writerow(['Product Code', 'Price', 'Quantity'])
        writer.writerows(all_products)
    
    print("CSV generation complete.")

# Call the function
fetch_all_products()
