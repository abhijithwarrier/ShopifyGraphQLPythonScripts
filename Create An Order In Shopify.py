"""
Programmer - python_scripts (Abhijith Warrier)

PYTHON SCRIPT TO CREATE AN ORDER IN Shopify USING GraphQL Admin API

This script demonstrates how to create an order in Shopify using the GraphQL Admin API.
It includes customer details, billing and shipping addresses, and line items.

1. Create Order - Uses the orderCreate mutation to create an order with all necessary details.
2. Retrieve Order - Fetches the order details after creation to verify a successful creation.

Orders are fundamental transactions in Shopify, and this script provides an automated way
of handling order creation via API.
"""

# Importing necessary packages
import json
import requests

# Shopify Admin API details
SHOP_URL = "<your_store_name>.myshopify.com"
ACCESS_TOKEN = "<your_store_access_token>"
API_VERSION = "2025-01"  # Update as per latest supported version
GRAPHQL_URL = f"https://{SHOP_URL}/admin/api/{API_VERSION}/graphql.json"

# Function to create an Order in Shopify with the provided Customer Data and Line Items Data
def create_order(line_items, customer_details, billing_address, shipping_address):
    """
    Creates an order in Shopify.

    Returns:
    JSON response containing the created order details or error messages
    """
    mutation = """
    mutation OrderCreate($order: OrderCreateOrderInput!) {
        orderCreate(order: $order) {
            order {
                id
                name
                email                                   # Email ID of the Customer
                customer {
                    firstName                           # First name of the Customer
                    lastName                            # Last name of the Customer
                    email                               # Email ID of the Customer
                    phone                               # Contact Number of the Customer
                }
                billingAddress {                        # Billing Address Details (dict)
                    firstName
                    lastName
                    address1
                    address2
                    city
                    province
                    country
                    zip
                    phone
                }
                shippingAddress {                       # Shipping Address Details (dict)
                    firstName
                    lastName
                    address1
                    address2
                    city
                    province
                    country
                    zip
                    phone
                }
                lineItems(first: 5) {                   # List of Product Line Items in the Order
                    edges {
                        node {
                            title
                            quantity
                            originalUnitPriceSet {
                                presentmentMoney {
                                    amount
                                    currencyCode
                                }
                            }
                        }
                    }
                }
                totalPriceSet {
                    presentmentMoney {
                        amount
                        currencyCode
                    }
                }
            }
            userErrors {
                field
                message
            }
        }
    }
    """

    # GraphQL variables containing the Customer Details and Line Items Details
    variables = {
        "order": {
            "email": customer_details["email"],
            "billingAddress": billing_address,
            "shippingAddress": shipping_address,
            "lineItems": line_items,
        }
    }

    # Sending the mutation request to Shopify GraphQL API
    response = requests.post(
        GRAPHQL_URL,
        json={"query": mutation, "variables": variables},
        headers={"X-Shopify-Access-Token": ACCESS_TOKEN, "Content-Type": "application/json"},
    )
    return response.json()

# Details of the Products & Quantity to be associated with the Order
line_items = [
    {
        "variantId": "gid://shopify/ProductVariant/47696106127597",
        "quantity": 1
    },
    {
        "variantId": "gid://shopify/ProductVariant/47696108355821",
        "quantity": 2
    }
]

# Example of Customer Data for creating an Order in Shopify
customer_details = {
    "email": "abhijith@example.com",
}
billing_address = shipping_address = {
    "firstName": "Abhijith",
    "lastName": "W",
    "address1": "123 Main St",
    "address2": "Apartment 4B",
    "city": "Bangalore",
    "province": "Karnataka",
    "country": "India",
    "zip": "560076",
    "phone": "+911234567890"
}

# Create an order and print the response
order_response = create_order(line_items, customer_details, billing_address, shipping_address)
print("Order Creation Response:", json.dumps(order_response, indent=2))
