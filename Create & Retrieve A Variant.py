"""
Programmer - python_scripts (Abhijith Warrier)

PYTHON SCRIPT TO CREATE & RETRIEVE NEW VARIANT FOR PRODUCT IN Shopify USING GraphQL Admin API

This script demonstrates how to manage product variants in Shopify using the GraphQL Admin API.
It performs the following steps:

	1.	Retrieve Product Details with Existing Variants – The script first fetches a product’s
	    details along with its existing variants.
	2.	Create a New Variant for the Product – It then adds a new variant to the product by
	    specifying attributes such as SKU, price, and option values.
	3.	Retrieve the Updated Product – After adding the variant, the script fetches the product
	    details again to confirm that the new variant has been successfully added.

This ensures that variants are correctly created and associated with the product while adhering
to Shopify’s API structure.
"""

# Importing the necessary packages
import json
import requests

# Shopify Admin API details
SHOP_URL = "your_store_name.myshopify.com"
ACCESS_TOKEN = "<your_access_token>"
API_VERSION = "2024-01"  # Update as per latest supported version
GRAPHQL_URL = f"https://{SHOP_URL}/admin/api/{API_VERSION}/graphql.json"

# Headers for authentication
HEADERS = {
    "X-Shopify-Access-Token": ACCESS_TOKEN,
    "Content-Type": "application/json",
}

# Function to retrieve the existing Variants of a Product
def retrieve_product_variants(product_id):
    """
    Retrieves all variants of a given product by its ID.
    """
    query = """
        query getProduct($id: ID!) {
            product(id: $id) {
                id
                title
                variants(first: 10) {
                    edges {
                        node {
                            id
                            title  # Variant title
                            sku
                            price
                        }
                    }
                }
            }
        }
    """
    variables = {"id": product_id}
    response = requests.post(GRAPHQL_URL, json={"query": query, "variables": variables}, headers=HEADERS)
    return response.json()

def create_variant(product_id, sku, price, title):
    """
    Creates a new variant for a given product.
    """
    mutation = """
        mutation createVariant($input: ProductVariantInput!) {
            productVariantCreate(input: $input) {
                productVariant {
                    id
                    title  # Variant title
                    sku
                    price
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
            "productId": product_id,
            "sku": sku,
            "price": price,
            "options": [title]  # Assign title to variant
        }
    }
    response = requests.post(GRAPHQL_URL, json={"query": mutation, "variables": variables}, headers=HEADERS)
    return response.json()

# Define the parameters and values for creating the new Variant
product_id = "gid://shopify/Product/8941400326381"
sku = "PTP-PS-VAR369"
price = "500.00"
variant_title = "1L"

# Retrieve existing variants
print("Existing Variants:", json.dumps(retrieve_product_variants(product_id), indent=2))

# Create new variant
print("Creating New Variant:", json.dumps(create_variant(product_id, sku, price, variant_title), indent=2))

# Retrieve updated variants
print("New Variants:", json.dumps(retrieve_product_variants(product_id), indent=2))


"""
Existing Variants: {
  "data": {
    "product": {
      "id": "gid://shopify/Product/8941400326381",
      "title": "Python Test Product - 17/02",
      "variants": {
        "edges": [
          {
            "node": {
              "id": "gid://shopify/ProductVariant/47751022149869",
              "title": "250ml",
              "sku": "PTP-UI-VARIANT",
              "price": "200.00"
            }
          }
        ]
      }
    }
  },
  "extensions": {
    "cost": {
      "requestedQueryCost": 7,
      "actualQueryCost": 4,
      "throttleStatus": {
        "maximumAvailable": 2000.0,
        "currentlyAvailable": 1996,
        "restoreRate": 100.0
      }
    }
  }
}
Creating New Variant: {
  "data": {
    "productVariantCreate": {
      "productVariant": {
        "id": "gid://shopify/ProductVariant/47751036469485",
        "title": "1L",
        "sku": "PTP-PS-VAR369",
        "price": "500.00"
      },
      "userErrors": []
    }
  },
  "extensions": {
    "cost": {
      "requestedQueryCost": 10,
      "actualQueryCost": 10,
      "throttleStatus": {
        "maximumAvailable": 2000.0,
        "currentlyAvailable": 1990,
        "restoreRate": 100.0
      }
    }
  }
}
New Variants: {
  "data": {
    "product": {
      "id": "gid://shopify/Product/8941400326381",
      "title": "Python Test Product - 17/02",
      "variants": {
        "edges": [
          {
            "node": {
              "id": "gid://shopify/ProductVariant/47751022149869",
              "title": "250ml",
              "sku": "PTP-UI-VARIANT",
              "price": "200.00"
            }
          },
          {
            "node": {
              "id": "gid://shopify/ProductVariant/47751036469485",
              "title": "1L",
              "sku": "PTP-PS-VAR369",
              "price": "500.00"
            }
          }
        ]
      }
    }
  },
  "extensions": {
    "cost": {
      "requestedQueryCost": 7,
      "actualQueryCost": 4,
      "throttleStatus": {
        "maximumAvailable": 2000.0,
        "currentlyAvailable": 1996,
        "restoreRate": 100.0
      }
    }
  }
}
"""