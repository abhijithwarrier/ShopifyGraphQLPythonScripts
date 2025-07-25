"""
Programmer - python_scripts (Abhijith Warrier)

PYTHON SCRIPT TO REFUND AN ORDER IN SHOPIFY USING GraphQL ADMIN API

This script processes a refund for an existing Shopify order. It allows refunding specific line items or the
entire order and retrieves the updated order details to verify the refund status.

1. Retrieve Order – Fetch complete order details, including fulfillment status and line items.
2. Refund Order –   Process a refund for selected line items or entire order using the refundCreate mutation.
3. Verify Refund –  Retrieve the order again to confirm that the refund has been successfully applied.

Refund management is essential for handling returns, cancellations, and customer satisfaction efficiently.
"""

# Importing necessary packages
import json
import requests

# Shopify Admin API details
SHOP_URL = "<your_store_name>.myshopify.com"
ACCESS_TOKEN = "<your_access_token>"
API_VERSION = "2024-01"  # Update as per the latest supported version
GRAPHQL_URL = f"https://{SHOP_URL}/admin/api/{API_VERSION}/graphql.json"


# Function to retrieve an order
def retrieve_order(order_id):
    query = """
    query getOrder($id: ID!) {
        order(id: $id) {
            id                                          # Shopify Order ID
            name                                        # Shopify Order Name
            refunds {                                   # Shopify Order Refund Details
                id                                      # Shopify Order Refund ID
                note                                    # Shopify Order Refund Note
                createdAt                               # Shopify Order Refund Created At
            }
            totalRefundedSet {
                presentmentMoney {
                    amount                              # Total order amount before refund
                    currencyCode
                }
            }
            transactions {                              # Shopify Order Transactions
                id                                      # Shopify Order Transaction ID
                gateway                                 # Shopify Order Transaction Gateway
                kind                                    # Shopify Order Transaction Kind
                amount                                  # Shopify Order Transaction Amount
            }
            lineItems(first: 10) {
                edges {
                    node {
                        id                              # Line Item ID required for refunds
                        title                           # Product Title in the order
                        quantity                        # Quantity of the Product ordered
                        originalTotalSet {
                            presentmentMoney {
                                amount                  # Price per Product
                                currencyCode            # Currency of the price
                            }
                        }
                    }
                }
            }
        }
    }
    """

    variables = {"id": order_id}
    response = requests.post(GRAPHQL_URL, json={"query": query, "variables": variables},
                             headers={"X-Shopify-Access-Token": ACCESS_TOKEN})
    return response.json()


# Function to refund an order
def refund_order(order_id, refund_line_items, order_transaction_details):
    mutation = """
    mutation orderRefundCreate($input: RefundInput!) {
        refundCreate(input: $input) {
            refund {
                id                                                      # Shopify Refund ID
                note
                totalRefundedSet {                                      # Total Refunded Amount
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

    variables = {
        "input": {
            "orderId": order_id,                                        # The Shopify Order GID to refund
            "note": "Testing Refund using Python with GraphQL API",     # Optional Reason for Refund
            "refundLineItems": refund_line_items,                       # List of line items to refund
            "notify": True,                                             # Notify customer about the refund
            "shipping": {"fullRefund": True},                           # Refunding shipping costs
            "transactions": order_transaction_details,
        }
    }
    response = requests.post(GRAPHQL_URL, json={"query": mutation, "variables": variables},
                             headers={"X-Shopify-Access-Token": ACCESS_TOKEN})
    return response.json()


# Step 1: Retrieve the order details from Shopify using the order ID
# Example order ID (must be replaced with an actual order GID)
order_id = "gid://shopify/Order/6188303286509"
# Fetch full order details, including line items
order_details = retrieve_order(order_id)
print("Order Details:", json.dumps(order_details, indent=2))

# Step 2: Select line items to be refunded
# Refund 1 unit of each item from the retrieved order
refund_line_items = [
    {"lineItemId": line["node"]["id"], "quantity": 1}
    for line in order_details["data"]["order"]["lineItems"]["edges"]
]

# Step 3: Retrieve the transaction details
# Set the kind as "REFUND"
order_transaction_details = [
    {"orderId": order_id, "gateway": transaction["gateway"], "kind": "REFUND",
     "amount": transaction["amount"], "parentId": transaction["id"]}
    for transaction in order_details["data"]["order"]["transactions"]
]

# Step 4: Process the refund by calling the refund_order mutation
# Initiate refund request for selected items
refund_response = refund_order(order_id, refund_line_items, order_transaction_details)
# Output the refund response for verification
print("Refund Response:", json.dumps(refund_response, indent=4))

# Step 5: Verify the refund by retrieving the updated order details
# Fetch the order again to check if the refund was applied
updated_order = retrieve_order(order_id)
# Output updated order details to confirm refund
print("Updated Order Details:", json.dumps(updated_order, indent=4))
