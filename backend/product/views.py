# HAVE BEEN SEPARATED INTO CSR PATTERN
# # from django.shortcuts import render
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework import status

# # Global list to store products temporarily
# products = []
# next_id = 1  # Auto-incrementing ID for products


# def validate_product_data(data, is_update=False, existing_product=None):
#     """
#     Validate product data before saving.
    
#     - is_update: If True, validation is for an update (PUT).
#     - existing_product: Pass the current product when updating.
#     """
    
#     required_fields = ["name", "description", "category", "price", "brand", "quantity"]
    
#     # Check for missing fields (only for new product creation)
#     if not is_update:
#         for field in required_fields:
#             if field not in data or not str(data[field]).strip():
#                 return {"error": f"{field.capitalize()} cannot be empty."}
    
#     # Validate name (should not be empty or duplicate)
#     if "name" in data:
#         if not data["name"].strip():
#             return {"error": "Product name cannot be empty."}
#         if not is_update and any(p["name"] == data["name"] for p in products):
#             return {"error": "A product with this name already exists."}
#         if is_update and data["name"] != existing_product["name"] and any(p["name"] == data["name"] for p in products):
#             return {"error": "A product with this name already exists."}

#     # Validate description
#     if "description" in data and not data["description"].strip():
#         return {"error": "Description cannot be empty."}
    
#     # Validate category
#     if "category" in data and not data["category"].strip():
#         return {"error": "Category cannot be empty."}
    
#     # Validate price (should be greater than zero)
#     if "price" in data:
#         try:
#             price = float(data["price"])
#             if price <= 0:
#                 return {"error": "Price must be greater than zero."}
#         except ValueError:
#             return {"error": "Price must be a valid number."}

#     # Validate brand
#     if "brand" in data and not data["brand"].strip():
#         return {"error": "Brand cannot be empty."}

#     # Validate quantity (should be a positive integer and greater than zero)
#     if "quantity" in data:
#         try:
#             quantity = int(data["quantity"])
#             if quantity <= 0:
#                 return {"error": "Quantity must be a positive integer greater than zero."}
#         except ValueError:
#             return {"error": "Quantity must be a valid integer."}

#     return None  # No errors


# class ProductListView(APIView):
#     """Handles fetching all products and adding a new product (in-memory)."""

#     def get(self, request):
#         """Fetch the list of all products."""
#         return Response(products, status=status.HTTP_200_OK)

#     def post(self, request):
#         """Create a new product with validation."""
#         global next_id
#         data = request.data

#         # Validate product data
#         validation_error = validate_product_data(data)
#         if validation_error:
#             return Response(validation_error, status=status.HTTP_400_BAD_REQUEST)

#         # Assign an auto-incremented ID and add to the list
#         data["id"] = next_id
#         next_id += 1
#         products.append(data)

#         return Response(data, status=status.HTTP_201_CREATED)


# class ProductDetailView(APIView):
#     """Handles fetching, updating, and deleting a specific product (in-memory)."""

#     def get(self, request, product_id):
#         """Fetch a specific product by ID."""
#         product = next((p for p in products if p["id"] == product_id), None)
#         if not product:
#             return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
#         return Response(product, status=status.HTTP_200_OK)

#     def put(self, request, product_id):
#         """Update a product by ID."""
#         product = next((p for p in products if p["id"] == product_id), None)
#         if not product:
#             return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

#         data = request.data

#         # Validate product data
#         validation_error = validate_product_data(data, is_update=True, existing_product=product)
#         if validation_error:
#             return Response(validation_error, status=status.HTTP_400_BAD_REQUEST)

#         # Update product details
#         product.update(data)
#         return Response(product, status=status.HTTP_200_OK)

#     def delete(self, request, product_id):
#         """Delete a product by ID."""
#         global products
#         product = next((p for p in products if p["id"] == product_id), None)
#         if not product:
#             return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

#         products = [p for p in products if p["id"] != product_id]
#         return Response({"message": "Product deleted"}, status=status.HTTP_204_NO_CONTENT)
