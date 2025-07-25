"""
Programmer - python_scripts (Abhijith Warrier)

PYTHON SCRIPT TO DELETE A PRODUCT FROM Shopify AND TRY RETRIEVING IT USING GraphQL Admin API

This script demonstrates how to delete a product from Shopify using the GraphQL Admin API.

It first sends a mutation request to delete a specific product by its ID. After the deletion,
it attempts to retrieve the same product to verify its removal from the store.

If the product is successfully deleted, Shopify will return an error or null response when
trying to fetch it. This process ensures that the product no longer exists in the store’s catalog.
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

# Function to delete a product
def delete_product(product_id):
    mutation = """
    mutation productDelete($id: ID!) {
      productDelete(input: {id: $id}) {
        deletedProductId  # The ID of the deleted product
        userErrors {
          field  # The field that caused the error (if any)
          message  # The error message
        }
      }
    }
    """

    # Set up request headers
    headers = {
        "Content-Type": "application/json",
        "X-Shopify-Access-Token": ACCESS_TOKEN,
    }

    # Request payload with the product ID
    payload = {
        "query": mutation,
        "variables": {"id": product_id}
    }

    # Send the API Request for deleting the product
    response = requests.post(GRAPHQL_URL, json=payload, headers=headers)

    return response.json()

# Function to retrieve product details
def retrieve_product(product_id):
    query = """
    query getProduct($id: ID!) {
      product(id: $id) {
        id  # The ID of the product
        title  # The title of the product
        descriptionHtml  # The description of the product
      }
    }
    """
    variables = {"id": product_id}

    # API Request to try retrieving the deelted product
    response = requests.post(GRAPHQL_URL,
                             json={"query": query, "variables": variables},
                             headers=HEADERS)
    return response.json()

# Replace with actual product ID
product_id = "gid://shopify/Product/<your_product_id>"

delete_response = delete_product(product_id)
print("Delete Response:", json.dumps(delete_response, indent=2))

print("After Deleting:", json.dumps(retrieve_product(product_id), indent=2))

