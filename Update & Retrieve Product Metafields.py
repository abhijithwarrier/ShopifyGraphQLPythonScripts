"""
Programmer - python_scripts (Abhijith Warrier)

PYTHON SCRIPT TO UPDATE & RETRIEVE PRODUCT METAFIELDS IN Shopify USING GraphQL Admin API

This script retrieves all metafields of a Shopify product, updates a specific metafield,
and verifies the update by retrieving the metafields again. It demonstrates how to manage
product metafields using Shopify’s GraphQL API with Python.
	1.	Update Metafield – Update an existing Metafield using metafieldsSet mutation.
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
SHOP_URL = "<your_store_domain>.myshopify.com"
ACCESS_TOKEN = "<your_access_token>"
API_VERSION = "2024-01"  # Update as per latest supported version
GRAPHQL_URL = f"https://{SHOP_URL}/admin/api/{API_VERSION}/graphql.json"

# Function to retrieve all metafields of a product
def retrieve_product_metafields(product_id):
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
                        id          # Unique metafield ID
                        namespace   # Namespace categorizing the metafield
                        key         # Unique key to identify the metafield
                        value       # Stored value of the metafield
                        type        # Type of data stored in the metafield
                    }
                }
            }
        }
    }
    """
    variables = {"id": product_id}  # GraphQL variables containing the product ID

    # Sending the request to Shopify GraphQL API
    response = requests.post(
        GRAPHQL_URL,
        json={"query": query, "variables": variables},
        headers={"X-Shopify-Access-Token": ACCESS_TOKEN, "Content-Type": "application/json"},
    )
    return response.json()

# Function to update metafield of a product
def update_product_metafield(product_id, namespace, key, value, value_type):
    """
    Updates an existing metafield for a product.
    """
    mutation = """
    mutation updateMetafield($metafields: [MetafieldsSetInput!]!) {
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
                "ownerId": product_id,      # Associate the metafield with the product
                "namespace": namespace,     # Define the category/namespace for the metafield
                "key": key,                 # Unique identifier for the metafield
                "value": value,             # The value stored in the metafield
                "type": value_type          # The type of value being stored
            }
        ]
    }

    # Sending the mutation request to Shopify GraphQL API
    response = requests.post(
        GRAPHQL_URL,
        json={"query": mutation, "variables": variables},
        headers={"X-Shopify-Access-Token": ACCESS_TOKEN, "Content-Type": "application/json"},
    )
    return response.json()

# Define parameters and values for creating the new Metafield
product_id = "gid://shopify/Product/<your_product_id>"  # Replace with actual product GID
namespace = "custom"                                    # Namespace where metafield is stored
key_to_update = "origin"                                # Key of the metafield to update
updated_value = "Python with GraphQL API"               # New value to update the metafield
value_type = "single_line_text_field"                   # Data type of the metafield

# Retrieve and print existing metafields before updating
retrieved_metafield_response = retrieve_product_metafields(product_id)
print("Existing Product Metafields:", json.dumps(retrieved_metafield_response, indent=2))

# Checking if metafields exist before updating
if retrieved_metafield_response["data"]["product"]["metafields"]["edges"]:
    metafields = retrieved_metafield_response["data"]["product"]["metafields"]["edges"]

    # Loop through metafields to find the one to update
    for metafield in metafields:
        if metafield["node"]["key"].lower() == key_to_update.lower():
            # Trigger the update operation
            update_response = update_product_metafield(product_id, namespace, key_to_update, updated_value, value_type)
            print("Metafield update response:", json.dumps(update_response, indent=2))

    # Retrieve metafields again after update to confirm changes
    retrieved_metafields_after_update = retrieve_product_metafields(product_id)
    print("Metafields after update:", json.dumps(retrieved_metafields_after_update, indent=2))

else:
    print("No metafields found for the product.")

"""
Existing Product Metafields: {
  "data": {
    "product": {
      "id": "gid://shopify/Product/8941400326381",
      "title": "Python Test Product - 17/02",
      "metafields": {
        "edges": [
          {
            "node": {
              "id": "gid://shopify/Metafield/40607250645229",
              "namespace": "custom",
              "key": "Active",
              "value": "True",
              "type": "single_line_text_field"
            }
          },
          {
            "node": {
              "id": "gid://shopify/Metafield/40607256314093",
              "namespace": "custom",
              "key": "Origin",
              "value": "Python API",
              "type": "single_line_text_field"
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
Metafield update response: {
  "data": {
    "metafieldsSet": {
      "metafields": [
        {
          "id": "gid://shopify/Metafield/40607256314093",
          "namespace": "custom",
          "key": "origin",
          "value": "Python with GraphQL API",
          "type": "single_line_text_field"
        }
      ],
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
Metafields after update: {
  "data": {
    "product": {
      "id": "gid://shopify/Product/8941400326381",
      "title": "Python Test Product - 17/02",
      "metafields": {
        "edges": [
          {
            "node": {
              "id": "gid://shopify/Metafield/40607250645229",
              "namespace": "custom",
              "key": "Active",
              "value": "True",
              "type": "single_line_text_field"
            }
          },
          {
            "node": {
              "id": "gid://shopify/Metafield/40607256314093",
              "namespace": "custom",
              "key": "Origin",
              "value": "Python with GraphQL API",
              "type": "single_line_text_field"
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