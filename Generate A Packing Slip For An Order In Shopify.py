"""
Programmer - python_scripts (Abhijith Warrier)

PYTHON SCRIPT TO GENERATE A PACKING SLIP FOR AN ORDER IN SHOPIFY AND VIEW ITS DETAILS

This script retrieves full order details from Shopify, including the order name, billing & shipping address,
created date, line items, subtotal, shipping, tax, and total. It then generates a fully formatted packing slip
as a PDF using ReportLab, which can be saved, printed, or emailed as needed.

    1. Retrieve Order & Fulfillment Data – Fetches order details using the GraphQL Admin API.
    2. Generate Packing Slip PDF – Lays out all essential info including logo, order summary,
       customer address, item list, and totals.
    3. Saves a PDF – The packing slip is saved with the order number as filename.

Install the ReportLab Packing using the Command - pip install reportlab
"""

import requests
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

# Shopify Admin API details
SHOP_URL = "<your_store_name>.myshopify.com"  # Replace with your store domain
ACCESS_TOKEN = "<your_store_access_token>"
API_VERSION = "2024-01"
GRAPHQL_URL = f"https://{SHOP_URL}/admin/api/{API_VERSION}/graphql.json"

# Function to retrieve full order details
def get_order_details(order_id):
    query = """
    query getOrder($id: ID!) {                          # Accepts order ID as a variable (GraphQL GID format)
        order(id: $id) {                                # Retrieve the order object by its ID
            id
            name
            createdAt                                   # Timestamp of order creation
            billingAddress {                            # Customer's billing address details
                name
                address1
                address2
                city
                province
                country
                zip
                phone
            }
            shippingAddress {                           # Customer's shipping address details
                name
                address1
                address2
                city
                province
                country
                zip
                phone
            }
            currentSubtotalPriceSet {                   # Total of all items before tax/shipping
                shopMoney {
                    amount
                    currencyCode
                }
            }
            totalShippingPriceSet {                     # Shipping cost
                shopMoney {
                    amount
                    currencyCode
                }
            }
            totalTaxSet {                               # Total tax amount
                shopMoney {
                    amount
                    currencyCode
                }
            }
            totalPriceSet {                             # Final total (subtotal + tax + shipping)
                shopMoney {
                    amount
                    currencyCode
                }
            }
            lineItems(first: 10) {                      # Retrieves first 10 line items of the order
                edges {
                    node {
                        title
                        quantity
                        sku
                        originalUnitPriceSet {
                            shopMoney {
                                amount
                            }
                        }
                    }
                }
            }
        }
    }
    """

    # Sending the request to Shopify GraphQL API
    variables = {"id": order_id}
    headers = {
        "Content-Type": "application/json",
        "X-Shopify-Access-Token": ACCESS_TOKEN
    }
    response = requests.post(GRAPHQL_URL, headers=headers, json={"query": query, "variables": variables})
    return response.json()

# Function to generate a detailed packing slip PDF
def generate_packing_slip_pdf(order):
    file_name = f"PackingSlip_{order['name'].replace('#', '')}.pdf"
    c = canvas.Canvas(file_name, pagesize=letter)
    width, height = letter
    y = height - inch

    # Store Name (centered)
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width / 2, y - 50, "<your_store_name>")
    y -= 80

    # Order Summary
    c.setFont("Helvetica", 12)
    c.drawString(50, y, f"Order: {order['name']}")
    c.drawRightString(width - 50, y, f"Order Date: {order['createdAt'][:10]}")
    y -= 25

    # Billing & Shipping Address side-by-side
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y, "Billing Address")
    c.drawRightString(width - 50, y, "Shipping Address")
    y -= 15

    c.setFont("Helvetica", 9)
    bill = order['billingAddress'] or {}
    ship = order['shippingAddress'] or {}
    for i in range(6):
        by = bill.get("name", "") if i == 0 else bill.get(f"address{i}", "") or ""
        sy = ship.get("name", "") if i == 0 else ship.get(f"address{i}", "") or ""
        if i == 3:
            by = f"{bill.get('city', '')}, {bill.get('province', '')} {bill.get('zip', '')}"
            sy = f"{ship.get('city', '')}, {ship.get('province', '')} {ship.get('zip', '')}"
        elif i == 4:
            by = bill.get('country', '')
            sy = ship.get('country', '')
        elif i == 5:
            by = f"Phone: {bill.get('phone', '')}"
            sy = f"Phone: {ship.get('phone', '')}"

        c.drawString(50, y, by)
        c.drawRightString(width - 50, y, sy)
        y -= 12

    y -= 20

    # Line items
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y, "Items:")
    y -= 20
    c.setFont("Helvetica-Bold", 9)
    c.drawString(60, y, "Title")
    c.drawCentredString(300, y, "SKU")
    c.drawCentredString(380, y, "Qty")
    c.drawRightString(width - 60, y, "Price")
    y -= 12
    c.line(50, y, width - 50, y)
    y -= 10

    c.setFont("Helvetica", 9)
    for edge in order['lineItems']['edges']:
        item = edge['node']
        c.drawString(60, y, item['title'])
        c.drawCentredString(300, y, item['sku'] or "-")
        c.drawCentredString(380, y, str(item['quantity']))
        c.drawRightString(width - 60, y, f"₹{item['originalUnitPriceSet']['shopMoney']['amount']}")
        y -= 15

    y -= 10
    c.line(50, y, width - 50, y)
    y -= 25

    # Totals
    c.setFont("Helvetica-Bold", 10)
    c.drawRightString(width - 150, y, "Subtotal:")
    c.drawRightString(width - 60, y, f"₹{order['currentSubtotalPriceSet']['shopMoney']['amount']}")
    y -= 15
    c.drawRightString(width - 150, y, "Shipping:")
    c.drawRightString(width - 60, y, f"₹{order['totalShippingPriceSet']['shopMoney']['amount']}")
    y -= 15
    c.drawRightString(width - 150, y, "Tax:")
    c.drawRightString(width - 60, y, f"₹{order['totalTaxSet']['shopMoney']['amount']}")
    y -= 15
    c.drawRightString(width - 150, y, "Total:")
    c.drawRightString(width - 60, y, f"₹{order['totalPriceSet']['shopMoney']['amount']}")

    # Footer
    c.setFont("Helvetica-Oblique", 9)
    c.drawString(50, 40, "Thank you for your purchase! This is a system-generated packing slip.")
    c.save()
    print(f"Packing slip PDF saved as: {file_name}")

# Example usage (replace with actual Order's Shopify IDs)
order_id = "gid://shopify/Order/6193832886509"
# Retrieve the order details
order_data = get_order_details(order_id)
order_info = order_data["data"]["order"]
# Trigger the function to generate packing slip for the Order
generate_packing_slip_pdf(order_info)
