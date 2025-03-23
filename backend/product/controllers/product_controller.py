from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from product.services.product_service import ProductService
from product.serializers import ProductSerializer
from mongoengine import DoesNotExist, ValidationError, NotUniqueError


class ProductController(APIView):
    """Handles HTTP requests for product management."""

    def get(self, request, product_id=None):
        """Fetch all products or a single product by ID."""
        try:
            if product_id:
                product = ProductService.get_product_by_id(product_id)
                if product:
                    # Serialize the single product
                    serializer = ProductSerializer(product)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

            # Fetch all products
            products = ProductService.get_all_products()
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except (ValidationError, DoesNotExist) as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        """Create a new product."""
        try:
            # Use serializer for validation
            serializer = ProductSerializer(data=request.data)
            
            if serializer.is_valid():
                product = ProductService.create_product(serializer.validated_data)
                serializer = ProductSerializer(product)  # Serialize saved product
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except (ValidationError, NotUniqueError, ValueError) as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, product_id):
        """Update an existing product."""
        try:
            product = ProductService.get_product_by_id(product_id)

            if not product:
                return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

            # Use serializer for validation
            serializer = ProductSerializer(product, data=request.data, partial=True)
            
            if serializer.is_valid():
                updated_product = ProductService.update_product(product_id, serializer.validated_data)
                serializer = ProductSerializer(updated_product)
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except (ValidationError, NotUniqueError, ValueError) as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, product_id):
        """Delete a product."""
        try:
            deleted = ProductService.delete_product(product_id)
            
            if deleted:
                return Response({"message": "Product deleted"}, status=status.HTTP_204_NO_CONTENT)
            
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
