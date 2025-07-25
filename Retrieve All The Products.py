"""
Programmer - python_scripts (Abhijith Warrier)

PYTHON SCRIPT TO ALL THE PRODUCTS FROM Shopify USING GraphQL Admin API

This script retrieves all products from a Shopify store using the GraphQL Admin API.
It queries essential product details, such as the product title, description, and
associated variants, including SKU and price. The data is then formatted and displayed,
allowing store owners to easily review their product catalog.
This approach is efficient for bulk product retrieval and can be useful for inventory
management, reporting, or further processing within a Shopify app or automation script.
"""

# Importing the necessary packages
import json
import requests

# Shopify Store Credentials (Replace with your actual store and token)
SHOPIFY_STORE = "your_shop.myshopify.com"
ACCESS_TOKEN = "<your_access_token>"
API_VERSION = "2024-01"

# Shopify GraphQL API URL
GRAPHQL_URL = f"https://{SHOPIFY_STORE}/admin/api/{API_VERSION}/graphql.json"

# Headers for authentication
HEADERS = {
    "Content-Type": "application/json",
    "X-Shopify-Access-Token": ACCESS_TOKEN
}

# Function to send GraphQL request
def fetch_all_products():
    # GraphQL query to retrieve all products
    query = """
    {
      products(first: 10) {  # Fetch first 10 products (adjust as needed)
        edges {
          node {
            id  # Product ID
            title  # Product title
            descriptionHtml  # Product description
            variants(first: 5) {  # Fetch up to 5 variants per product
              edges {
                node {
                  id  # Variant ID
                  title  # Variant title
                  price  # Variant price
                  sku  # Variant SKU
                }
              }
            }
          }
        }
      }
    }
    """
    # Send the API Request for retrieving all the products
    response = requests.post(GRAPHQL_URL, headers=HEADERS, json={"query": query})
    return response.json()

products = fetch_all_products()
print("List Of Products:", json.dumps(products, indent=2))
