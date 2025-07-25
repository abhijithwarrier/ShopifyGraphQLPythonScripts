"""
Programmer - python_scripts (Abhijith Warrier)

PYTHON SCRIPT TO CREATE & RETRIEVE PRODUCT METAFIELDS IN Shopify USING GraphQL Admin API

This script focuses on creating & retrieving Metafields for a Shopify Product.
	1.	Create Metafield – Add a new Metafield to a product using metafieldsSet mutation.
	    Metafields allow you to store custom data beyond Shopify’s built-in attributes.

	2.	Retrieve Metafields – All metafields associated with the product are retrieved
	    to verify that the new metafield has been successfully added.

Metafields are useful for adding custom product details such as specifications, or
internal notes, making them a powerful tool for extending Shopify’s functionality.
"""

# Importing the necessary packages
import json
import requests

# Shopify Admin API details
SHOP_URL = "<your_store_name>.myshopify.com"
ACCESS_TOKEN = "<your_access_token>"
API_VERSION = "2024-01"  # Update as per latest supported version
GRAPHQL_URL = f"https://{SHOP_URL}/admin/api/{API_VERSION}/graphql.json"

# Function to create a metafield for a product
def create_metafield(product_id, namespace, key, value, value_type):
    """
    Creates a metafield for a given product.
    """
    mutation = """
    mutation createMetafield($metafields: [MetafieldsSetInput!]!) {
        metafieldsSet(metafields: $metafields) {
            metafields {
                id          # The unique Shopify product ID (GraphQL GID format)
                namespace   # The namespace to categorize the metafield
                key         # The unique key to identify the metafield
                value       # The actual data to store in the metafield
                type        # The data type of the metafield
            }
            userErrors {
                field
                message
            }
        }
    }
    """
    variables = {
        "metafields": [
            {
                "ownerId": product_id,  # Associate the metafield with the product
                "namespace": namespace,  # Define the category/namespace for the metafield
                "key": key,  # Unique identifier for the metafield
                "value": value,  # The value stored in the metafield
                "type": value_type  # The type of value being stored
            }
        ]
    }
    response = requests.post(
        GRAPHQL_URL,
        json={"query": mutation, "variables": variables},
        headers={"X-Shopify-Access-Token": ACCESS_TOKEN, "Content-Type": "application/json"},
    )
    return response.json()

# Function to retrieve all metafields of a product
def retrieve_metafields(product_id):
    """
    Retrieves all metafields for a given product.

    Arguments:
    product_id -- The unique Shopify product ID (GraphQL GID format)

    Returns:
    JSON response containing all metafields of the product
    """
    query = """
    query getProductMetafields($id: ID!) {
        product(id: $id) {
            id
            title
            metafields(first: 10) {  # Retrieves the product's metafields
                edges {
                    node {
                        id
                        namespace
                        key
                        value
                        type
                    }
                }
            }
        }
    }
    """
    variables = {"id": product_id}
    response = requests.post(
        GRAPHQL_URL,
        json={"query": query, "variables": variables},
        headers={"X-Shopify-Access-Token": ACCESS_TOKEN, "Content-Type": "application/json"},
    )
    return response.json()

# Define parameters and values for creating the new Metafield
product_id = "gid://shopify/Product/<your_product_id>"
namespace = "custom"
key = "Origin"
value = "Python API"
value_type = "single_line_text_field"

retrieve_response = retrieve_metafields(product_id)
print("Existing Product Metafields:", json.dumps(retrieve_response, indent=2))

# Create the Metafield
create_response = create_metafield(product_id, namespace,
                                   key, value, value_type)
print("New Metafield Created:", json.dumps(create_response, indent=2))

# Retrieve the Metafield
retrieve_response = retrieve_metafields(product_id)
print("Updated Product Metafields:", json.dumps(retrieve_response, indent=2))
