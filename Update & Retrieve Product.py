"""
Programmer - python_scripts (Abhijith Warrier)

PYTHON SCRIPT TO UPDATE & RETRIEVE PRODUCTS FROM Shopify USING GraphQL Admin API

This script interacts with the Shopify GraphQL Admin API to retrieve and update product details.
It is designed to perform the following operations:

1. `retrieve_product(product_id)`:
   - Fetches details of a specific product using its Shopify Product ID.
   - Retrieves key attributes such as title, description, price, and variants.

2. `update_product(product_id, new_title, new_description)`:
   - Updates the product's title or description using a GraphQL mutation.
   - Ensures that only the provided fields are updated while keeping other details unchanged.
   - Retrieves the updated product details to confirm the changes.

The script is structured for reusability and can be extended for bulk product updates.
"""

# Importing the necessary packages
import json
import requests

# Shopify Store Credentials (Replace with your actual store and token)
SHOPIFY_STORE = "your_store.myshopify.com"
ACCESS_TOKEN = "<your_store_access_token>"
API_VERSION = "2024-01"

# Shopify GraphQL API URL
GRAPHQL_URL = f"https://{SHOPIFY_STORE}/admin/api/{API_VERSION}/graphql.json"

# Headers for authentication
HEADERS = {
    "Content-Type": "application/json",
    "X-Shopify-Access-Token": ACCESS_TOKEN
}


# Function to retrieve product details
def retrieve_product(product_id):
    query = """
    query getProduct($id: ID!) {
      product(id: $id) {
        id
        title
        descriptionHtml
      }
    }
    """
    variables = {"id": product_id}

    response = requests.post(GRAPHQL_URL,
                             json={"query": query, "variables": variables},
                             headers=HEADERS)
    return response.json()


# Function to update product details
def update_product(product_id, new_title, new_description):
    mutation = """
    mutation updateProduct($id: ID!, $title: String!, $descriptionHtml: String!) {
      productUpdate(input: {
        id: $id,  # Product ID to be updated
        title: $title,  # New product title
        descriptionHtml: $descriptionHtml  # New product description
      }) {
        product {
          id  # Retrieve updated product ID
          title  # Retrieve updated product title
          descriptionHtml  # Retrieve updated product description
        }
        userErrors {
          field  # Field that caused an error, if any
          message  # Error message if update fails
        }
      }
    }
    """
    variables = {
        "id": product_id,
        "title": new_title,
        "descriptionHtml": new_description
    }

    response = requests.post(GRAPHQL_URL,
                             json={"query": mutation, "variables": variables},
                             headers=HEADERS)
    return response.json()


# Replace with actual product ID
product_id = "gid://shopify/Product/<your_product_id>"

print("Before Update:", json.dumps(retrieve_product(product_id), indent=2))

updated_response = update_product(
    product_id,
    "Updated Product Title",
    "<p>New product description</p>")
print("Update Response:", updated_response)

print("After Update:", json.dumps(retrieve_product(product_id), indent=2))

