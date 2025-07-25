"""
Programmer - python_scripts (Abhijith Warrier)

PYTHON SCRIPT TO RETRIEVE, DELETE & VERIFY PRODUCT METAFIELDS IN Shopify USING GraphQL Admin API

This script retrieves all metafields of a Shopify product, deletes a specific metafield,
and verifies the deletion by retrieving the metafields again. It demonstrates how to manage
product metafields using Shopify’s GraphQL API with Python.

1. Retrieve Metafields – Fetch all metafields associated with the product to check existing values.
2. Delete Metafield – Remove a specific metafield using metafieldDelete mutation.
3. Verify Metafield Deletion – Retrieve metafields again to ensure successful deletion.

Metafields are useful for adding custom product details such as specifications or internal notes,
making them a powerful tool for extending Shopify’s functionality.
"""

# Importing the necessary packages
import json
import requests

# Shopify Admin API details
SHOP_URL = "<your_store_name>.myshopify.com"
ACCESS_TOKEN = "<your_access_token>"
API_VERSION = "2024-01"
GRAPHQL_URL = f"https://{SHOP_URL}/admin/api/{API_VERSION}/graphql.json"

# Function to retrieve all metafields of a product
def retrieve_product_metafields(product_id):
    """
    Retrieves all metafields for a given product.
    Arguments: product_id -- The unique Shopify product ID (GraphQL GID format)
    Returns: JSON response containing all metafields of the product
    """
    query = """
    query getProductMetafields($id: ID!) {
        product(id: $id) {
            id
            title
            metafields(first: 10) {
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
    variables = {"id": product_id}      # GraphQL variables containing the product ID

    # Sending the request to Shopify GraphQL API
    response = requests.post(
        GRAPHQL_URL,
        json={"query": query, "variables": variables},
        headers={"X-Shopify-Access-Token": ACCESS_TOKEN, "Content-Type": "application/json"},
    )
    return response.json()

# Function to delete a metafield of a product
def delete_product_metafield(metafield_id):
    """
    Deletes a metafield using its unique Shopify ID.
    Arguments: metafield_id -- The unique Shopify metafield ID (GraphQL GID format)
    Returns: JSON response confirming deletion or returning an error message
    """
    mutation = """
    mutation deleteMetafield($id: ID!) {
        metafieldDelete(input: {id: $id}) {
            deletedId
            userErrors {
                field
                message
            }
        }
    }
    """
    variables = {"id": metafield_id}    # GraphQL variables containing the metafield ID

    # Sending the request to Shopify GraphQL API
    response = requests.post(
        GRAPHQL_URL,
        json={"query": mutation, "variables": variables},
        headers={"X-Shopify-Access-Token": ACCESS_TOKEN, "Content-Type": "application/json"},
    )
    return response.json()


# Define product details
product_id = "gid://shopify/Product/<your_product_id>"  # Replace with actual product GID
namespace = "custom"                                    # Namespace where metafield is stored
key_to_delete = "origin"                                # Key of the metafield to delete

# Retrieve and print existing metafields before deletion
retrieved_metafield_response = retrieve_product_metafields(product_id)
print("Existing Product Metafields:", json.dumps(retrieved_metafield_response, indent=2))

# Check if metafields exist before attempting deletion
if retrieved_metafield_response["data"]["product"]["metafields"]["edges"]:
    metafields = retrieved_metafield_response["data"]["product"]["metafields"]["edges"]

    # Loop through metafields to find the one to delete
    for metafield in metafields:
        if (
                metafield["node"]["namespace"].lower() == namespace.lower()
                and metafield["node"]["key"].lower() == key_to_delete.lower()
        ):
            metafield_id = metafield["node"]["id"]

            # Trigger the delete operation
            delete_response = delete_product_metafield(metafield_id)
            print("Metafield Deletion Response:", json.dumps(delete_response, indent=2))
            break

    # Retrieve metafields again after deletion to verify removal
    retrieved_metafields_after_deletion = retrieve_product_metafields(product_id)
    print("Metafields After Deletion:", json.dumps(retrieved_metafields_after_deletion, indent=2))
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
Metafield Deletion Response: {
  "data": {
    "metafieldDelete": {
      "deletedId": "gid://shopify/Metafield/40607256314093",
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
Metafields After Deletion: {
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