"""
Programmer - python_scripts (Abhijith Warrier)

PYTHON SCRIPT TO RETRIEVE, UPDATE & VERIFY AN ORDER IN SHOPIFY USING GraphQL ADMIN API

This script retrieves an existing Shopify order, updates specific order details (such as tags, or customer information),
and verifies the update by retrieving the order again.
This demonstrates how to manage orders efficiently using Shopify’s GraphQL API.

    1. Retrieve Order – Fetch complete order details, including customer details, billing & shipping address,
                        line items, and payment information.
    2. Update Order –   Modify order attributes such as tags, notes, or shipping details using orderUpdate mutation.
    3. Verify Update –  Retrieve the order again to confirm that changes have been successfully applied.

Order management is crucial for tracking purchases, updating information, and ensuring smooth transactions.
"""

# Importing necessary packages
import json
import requests

# Shopify Admin API details
SHOP_URL = "<your_store_name>.myshopify.com"
ACCESS_TOKEN = "<your_store_access_token>"
API_VERSION = "2024-01"  # Update as per the latest supported version
GRAPHQL_URL = f"https://{SHOP_URL}/admin/api/{API_VERSION}/graphql.json"


# Function to retrieve an order
def retrieve_order(order_id):
    """
    Retrieves complete details of an order using the order ID.
    Parameters:
    order_id (str): The unique Shopify order ID (GraphQL GID format)
    Returns:
    JSON response containing the order details
    """
    query = """
    query getOrder($id: ID!) {
        order(id: $id) {
            id                              # Unique order ID
            name                            # Order name (e.g., #1001)
            email                           # Customer's email associated with the order
            customer {
                firstName                   # Customer's first name
                lastName                    # Customer's last name
            }
            billingAddress {
                address1                    # Primary billing address
                address2                    # Secondary billing address
                city                        # Billing city
                province                    # Billing state/province
                country                     # Billing country
                zip                         # Billing postal/ZIP code
                phone                       # Billing phone number
            }
            shippingAddress {
                address1                    # Primary shipping address
                address2                    # Secondary shipping address
                city                        # Shipping city
                province                    # Shipping state/province
                country                     # Shipping country
                zip                         # Shipping postal/ZIP code
                phone                       # Shipping phone number
            }
            tags                            # Tags associated with this order
            note                            # Notes associated with this order
        }
    }
    """

    variables = {"id": order_id}            # GraphQL variables containing the order ID

    # Sending the request to Shopify GraphQL API
    response = requests.post(
        GRAPHQL_URL,
        json={"query": query, "variables": variables},
        headers={"X-Shopify-Access-Token": ACCESS_TOKEN, "Content-Type": "application/json"},
    )
    return response.json()


# Function to update order details
def update_order(order_id, updated_tags, updated_note):
    """
    Updates specific attributes of an order such as tags and notes.

    Parameters:
    order_id (str): The unique Shopify order ID (GraphQL GID format)
    updated_tags (list): List of new tags to be assigned to the order
    updated_note (str): The new note to update in the order

    Returns:
    JSON response confirming the update status
    """
    mutation = """
    mutation updateOrder($input: OrderInput!) {
        orderUpdate(input: $input) {
            order {
                id                          # Unique order ID
                tags                        # Updated tags
                note                        # Updated note
            }
            userErrors {
                field
                message
            }
        }
    }
    """

    variables = {
        "input": {
            "id": order_id,                 # Order ID to update
            "tags": updated_tags,           # New tags for the order
            "note": updated_note            # New note for the order
        }
    }

    # Sending the mutation request to Shopify GraphQL API
    response = requests.post(
        GRAPHQL_URL,
        json={"query": mutation, "variables": variables},
        headers={"X-Shopify-Access-Token": ACCESS_TOKEN, "Content-Type": "application/json"},
    )
    return response.json()


# Define order ID and updated values
order_id = "gid://shopify/Order/<order_id>"             # Replace with actual order GID
updated_tags = ["Priority", "Express Shipping"]         # Example tags
updated_note = "Customer requested express delivery."   # Example note update

# Step 1: Retrieve and print existing order details
retrieved_order = retrieve_order(order_id)
print("Existing Order Details:", json.dumps(retrieved_order, indent=2))

# Step 2: Update the order with new tags and note
update_response = update_order(order_id, updated_tags, updated_note)
print("Order Update Response:", json.dumps(update_response, indent=2))

# Step 3: Retrieve order again to verify updates
retrieved_order_after_update = retrieve_order(order_id)
print("Updated Order Details:", json.dumps(retrieved_order_after_update, indent=2))
