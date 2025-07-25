"""
Programmer - python_scripts (Abhijith Warrier)

PYTHON SCRIPT TO RETRIEVE ORDER DETAILS IN Shopify USING GraphQL Admin API

This script retrieves details of a specific order in Shopify using the GraphQL Admin API.
It fetches information such as customer details, billing and shipping addresses, line items,
and total price, making it useful for order verification, fulfillment, and customer support.

    1. Retrieve Order – Fetch complete order details using order ID.
    2. Includes Customer, Billing, and Shipping Information.
    3. Lists all Line Items in the Order.

This script helps in efficiently managing orders within Shopify by accessing structured data.
"""

# Importing necessary packages
import json
import requests

# Shopify Admin API details
SHOP_URL = "<your_store_name>.myshopify.com"
ACCESS_TOKEN = "<your_store_access_token>"
API_VERSION = "2025-01"  # Update as per latest supported version
GRAPHQL_URL = f"https://{SHOP_URL}/admin/api/{API_VERSION}/graphql.json"

# Function to retrieve order details
def retrieve_order(order_id):
    """
    Retrieves complete details of an order in Shopify.

    Arguments:
    order_id -- The unique Shopify order ID (GraphQL GID format).

    Returns:
    JSON response containing order details or error messages.
    """
    query = """
    query getOrder($id: ID!) {
        order(id: $id) {
            id                                      # Unique Shopify order ID
            name                                    # Shopify-generated order name (e.g., #1001)
            email                                   # Email ID of the Customer
            customer {
                firstName                           # First name of the Customer
                lastName                            # Last name of the Customer
                email                               # Email ID of the Customer
                phone                               # Contact Number of the Customer
            }
            billingAddress {
                firstName                           # First name on the billing address
                lastName                            # Last name on the billing address
                address1                            # Primary address line
                address2                            # Secondary address line (if any)
                city                                # City name
                province                            # Province or state
                country                             # Country name
                zip                                 # Zip or postal code
                phone                               # Phone number associated with billing address
            }
            shippingAddress {
                firstName                           # First name on the shipping address
                lastName                            # Last name on the shipping address
                address1                            # Primary address line
                address2                            # Secondary address line (if any)
                city                                # City name
                province                            # Province or state
                country                             # Country name
                zip                                 # Zip or postal code
                phone                               # Phone number associated with shipping address
            }
            lineItems(first: 5) {
                edges {
                    node {
                        title                       # Product title in the order
                        quantity                    # Quantity of the product ordered
                        originalUnitPriceSet {
                            presentmentMoney {
                                amount              # Price per unit
                                currencyCode        # Currency of the price
                            }
                        }
                    }
                }
            }
            totalPriceSet {
                presentmentMoney {
                    amount                          # Total order price
                    currencyCode                    # Currency of the total price
                }
            }
        }
    }
    """
    variables = {"id": order_id}                    # GraphQL variables containing the order ID

    # Sending the request to Shopify GraphQL API
    response = requests.post(
        GRAPHQL_URL,
        json={"query": query, "variables": variables},
        headers={"X-Shopify-Access-Token": ACCESS_TOKEN, "Content-Type": "application/json"},
    )
    return response.json()


# Define the Order ID to retrieve
order_id = "gid://shopify/Order/<your_order_id>"  # Replace with an actual Order GID

# Retrieve and print order details
order_response = retrieve_order(order_id)
print("Order Details:", json.dumps(order_response, indent=2))
