"""
Programmer - python_scripts (Abhijith Warrier)

PYTHON SCRIPT TO FULFILL AND VERIFY AN ORDER IN SHOPIFY USING GraphQL ADMIN API

This script automates the fulfillment of an order in Shopify and then verifies the fulfillment by retrieving
the order details again. It ensures that the specified line items are marked as fulfilled and that tracking
information is attached if provided.

    1. Retrieve Fulfillment Orders – Fetches fulfillment orders and related line items for a given Shopify order.
    2. Fulfill the Order – Uses fulfillmentCreateV2 mutation to fulfill specific line items with optional
                           tracking information.
    3. Verify Fulfillment – Retrieves the order post-fulfillment to confirm fulfillment status,
                            line items fulfillment, and tracking details.

Order fulfillment is essential for shipping processes and customer satisfaction, ensuring that orders are
properly processed and tracked.
"""

# Importing necessary packages
import json
import requests

# Shopify Admin API details
SHOP_URL = "<your_store_name>.myshopify.com"
ACCESS_TOKEN = "<your_store_access_token>"
API_VERSION = "2024-01"
GRAPHQL_URL = f"https://{SHOP_URL}/admin/api/{API_VERSION}/graphql.json"


# Function to retrieve fulfillmentOrderId and lineItems
def get_fulfillment_order(order_id):
    query = """
    query fulfillmentOrders($id: ID!) {
        order(id: $id) {
            fulfillmentOrders(first: 1) {
                edges {
                    node {
                        id                                  # fulfillmentOrderId
                        lineItems(first: 10) {              # List of line items
                            edges {
                                node {
                                    id                      # fulfillmentOrderLineItemId
                                    lineItem {              # Original line item details from the order
                                        title               # Product title
                                        quantity            # Quantity of the product ordered
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    """

    # Sending the request to Shopify GraphQL API
    response = requests.post(
        GRAPHQL_URL,
        json = {"query": query, "variables": { "id": order_id }},
        headers={"X-Shopify-Access-Token": ACCESS_TOKEN, "Content-Type": "application/json"},
    )
    return response.json()


# Function to fulfill an order in Shopify
def fulfill_order(fulfillment_order_id, line_item_ids):
    """
    Fulfills an order by specifying the order ID, line item ID(s), and location ID.

    Args:
        order_id (str): The Shopify ID of the order to fulfill
        line_item_id (str): The Shopify ID of the line item to fulfill
        location_id (str): The Shopify ID of the fulfillment location
    """
    mutation = """
    mutation fulfillmentCreateV2($fulfillment: FulfillmentV2Input!) {
        fulfillmentCreateV2(fulfillment: $fulfillment) {
            fulfillment {
                id                                              # Fulfillment ID
                status                                          # Fulfillment status (e.g., SUCCESS)
                trackingInfo {                                  # Tracking info object
                    number                                      # Tracking number
                    url                                         # Tracking URL
                }
            }
            userErrors {
                field                                           # Field where error occurred
                message                                         # Error message
            }
        }
    }
    """

    variables = {
        "fulfillment": {
            "trackingInfo": {
                "number": "1234567890",                             # Tracking number for the fulfillment
                "url": "https://tracking.example.com/1234567890"    # Tracking URL for the fulfillment
            },
            "lineItemsByFulfillmentOrder": [                        # List of fulfillment orders and their line items
                {
                    "fulfillmentOrderId": fulfillment_order_id,     # fulfillmentOrderId obtained from fulfillmentOrders
                    "fulfillmentOrderLineItems": [                  # List of line items to fulfill
                        { "id": line_item_id, "quantity": 1 } for line_item_id in line_item_ids
                    ]
                }
            ],
        }
    }

    # Sending the request to Shopify GraphQL API
    response = requests.post(
        GRAPHQL_URL,
        json={"query": mutation, "variables": variables},
        headers={"X-Shopify-Access-Token": ACCESS_TOKEN, "Content-Type": "application/json"},
    )
    return response.json()


# Function to retrieve the order to verify fulfillment
def retrieve_fulfilled_order(order_id):
    """
    Retrieves the order details to confirm fulfillment.

    Args:
        order_id (str): The Shopify ID of the order to retrieve
    """
    query = """
    query getOrder($id: ID!) {
        order(id: $id) {
            id                                                  # Shopify Order ID
            name                                                # Shopify Order Name (e.g., #1001)
            fulfillments(first: 5) {                            # Direct fulfillments for the order
                id                                              # Fulfillment ID
                status                                          # Status of the fulfillment
                createdAt                                       # Fulfillment creation date
                trackingInfo {                                  # Tracking info if available
                    number                                      # Tracking number
                    url                                         # Tracking URL
                }
            }
            fulfillmentOrders(first: 5) {                       # Fulfillment orders related to the order
                edges {
                    node {
                        id                                      # Fulfillment Order ID
                        status                                  # Status of the fulfillment order
                        createdAt                               # Creation date of fulfillment order
                        lineItems(first: 5) {                   # Line items inside fulfillment order
                            edges {
                                node {
                                    id                          # Fulfillment Order Line Item ID
                                    lineItem {
                                        title                   # Product title
                                        quantity                # Quantity of product
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    """

    # Sending the request to Shopify GraphQL API
    response = requests.post(
        GRAPHQL_URL,
        json={"query": query, "variables": {"id": order_id }},
        headers={"X-Shopify-Access-Token": ACCESS_TOKEN, "Content-Type": "application/json"},
    )
    return response.json()


# Example usage (replace with actual Order's Shopify IDs)
order_id = "gid://shopify/Order/6166080454893"

# Get fulfillment order details
fulfillment_data = get_fulfillment_order(order_id)
fulfillment_order_id = fulfillment_data["data"]["order"]["fulfillmentOrders"]["edges"][0]["node"]["id"]
line_items = fulfillment_data["data"]["order"]["fulfillmentOrders"]["edges"][0]["node"]["lineItems"]["edges"]
line_item_ids = [item["node"]["id"] for item in line_items]

# Trigger the function to fulfill an Order and print the Fulfillment Response
fulfillment_response = fulfill_order(fulfillment_order_id, line_item_ids)
print("Fulfillment Response:", json.dumps(fulfillment_response, indent=2))

# Trigger the function to retrieve the fulfilled Order and print the Order's Details
fulfilled_order_details = retrieve_fulfilled_order(order_id)
print("Order Details After Fulfillment:", json.dumps(fulfilled_order_details, indent=2))
