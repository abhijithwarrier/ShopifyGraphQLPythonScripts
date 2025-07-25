# Programmer - python_scripts (Abhijith Warrier)

# PYTHON SCRIPT TO CREATE & RETRIEVE PRODUCTS & VARIANTS FROM Shopify USING GraphQL Admin API

# This script automates the process of creating a product, adding a variant, and retrieving details using
# Shopify's Admin API with GraphQL.

# Steps:
# 1️⃣ Create a Product → Define product details like title, description, and metadata.
# 2️⃣ Add a Variant → Attach a variant to the product with SKU, price, and inventory details.
# 3️⃣ Retrieve Product Details → Fetch the product and its variants to verify creation.

# This approach ensures efficient data handling using GraphQL, reducing multiple API calls.

# Importing the necessary packages
import json
import requests

# Shopify Store Credentials (Replace with your actual store and token)
SHOPIFY_STORE = "your_store_name.myshopify.com"
ACCESS_TOKEN = "your_admin_api_access_token"

# Shopify GraphQL API URL
GRAPHQL_URL = f"https://{SHOPIFY_STORE}/admin/api/2024-01/graphql.json"

# Headers for authentication
HEADERS = {
    "Content-Type": "application/json",
    "X-Shopify-Access-Token": ACCESS_TOKEN
}


# Step 1: Create a Product in Shopify
def create_product():
    product_query = """
    mutation {
      productCreate(input: {
        title: "Python Generated Product",  # Product title
        descriptionHtml: "This is a product created via Python & GraphQL",  # Product description
        options: ["Title"],  # Required for multiple variants
        metafields: [{
          namespace: "custom",  # Metadata namespace
          key: "origin",  # Metadata key
          value: "Python API",  # Metadata value
          type: "single_line_text_field"  # Data type for metafield
        }]
      }) {
        product {
          id  # Retrieve product ID
          title  # Retrieve product title
        }
        userErrors {
          field  # Error field (if any)
          message  # Error message (if any)
        }
      }
    }
    """

    # Send GraphQL request
    product_response = requests.post(GRAPHQL_URL, headers=HEADERS, json={"query": product_query})
    data = product_response.json()

    # Handle errors
    if "errors" in data:
        print("Error creating product:", data["errors"])
        return None

    product_info = data.get("data", {}).get("productCreate", {})
    product_id = product_info.get("product", {}).get("id")

    if product_id:
        print(f"Product Created: {product_info['product']['title']} (ID: {product_id})")
        return product_id
    else:
        print("Failed to create product:", product_info.get("userErrors"))
        return None


# Step 2: Create a Variant for the Product
def create_variant(product_id):
    variant_query = """
    mutation productVariantCreate($productId: ID!) {
      productVariantCreate(input: {
        productId: $productId,  # Link variant to product
        title: "Python Variant",  # Variant title
        sku: "PYTHON-SKU-123",  # Variant SKU
        price: "29.99"  # Variant price
        options: ["Python Edition"]  # Must match product options
      }) {
        productVariant {
          id  # Retrieve variant ID
          sku  # Retrieve variant SKU
          price  # Retrieve variant price
        }
        userErrors {
          field  # Error field (if any)
          message  # Error message (if any)
        }
      }
    }
    """

    # Pass product ID dynamically
    variables = {"productId": product_id}

    # Send GraphQL request
    variant_response = requests.post(GRAPHQL_URL, headers=HEADERS, json={"query": variant_query, "variables": variables})
    data = variant_response.json()

    # Handle errors
    if "errors" in data:
        print("Error creating variant:", data["errors"])
        return None

    variant_info = data.get("data", {}).get("productVariantCreate", {})
    variant_id = variant_info.get("productVariant", {}).get("id")

    if variant_id:
        print(f"\nVariant Created: SKU {variant_info['productVariant']['sku']} (ID: {variant_id})")
    else:
        print("Failed to create variant:", variant_info.get("userErrors"))


# Retrieve the Created Product & Variant
def retrieve_product_variant(product_id):
    # GraphQL query to fetch the product details
    product_variant_query = f"""
    query {{
      product(id: "{product_id}") {{
        id
        title
        descriptionHtml
        variants(first: 5) {{
          edges {{
            node {{
              id
              title
              sku
              price
            }}
          }}
        }}
        metafields(first: 5) {{
          edges {{
            node {{
              namespace
              key
              value
            }}
          }}
        }}
      }}
    }}
    """

    # Sending the request to Shopify GraphQL API
    product_variant_response = requests.post(GRAPHQL_URL, json={"query": product_variant_query}, headers=HEADERS)
    retrieved_data = product_variant_response.json()  # Convert response to JSON
    print("\nRetrieved Product Details:", json.dumps(retrieved_data, indent=2))

# Execute the steps
product_id = create_product()  # Step 1: Create Product
if product_id:
    create_variant(product_id)  # Step 2: Add Variant (if product creation was successful)
if product_id:
    retrieve_product_variant(product_id)

