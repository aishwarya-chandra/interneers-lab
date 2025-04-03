from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from product.services.product_service import ProductService
from product.serializers import ProductSerializer
from mongoengine import DoesNotExist, ValidationError, NotUniqueError
from bson import ObjectId

class ProductController(APIView):
    """Handles HTTP requests for product management."""

    def get(self, request, product_id=None):
        """Fetch all products or a single product by ID."""
        try:
            if product_id:
                if not ObjectId.is_valid(product_id):
                    return Response({"error": "Invalid product ID."}, status=status.HTTP_400_BAD_REQUEST)
                
                product = ProductService.get_product_by_id(str(product_id))
                if product:
                    return Response(ProductSerializer(product).data, status=status.HTTP_200_OK)
                return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

            # Fetch all products
            products = ProductService.get_all_products()
            return Response(ProductSerializer(products, many=True).data, status=status.HTTP_200_OK)

        except (ValidationError, DoesNotExist, ValueError) as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        """Create a new product."""
        try:
            serializer = ProductSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            product = ProductService.create_product(serializer.validated_data)
            return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)

        except (ValidationError, NotUniqueError, ValueError) as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, product_id):
        """Update an existing product."""
        try:
            if not ObjectId.is_valid(product_id):
                return Response({"error": "Invalid product ID."}, status=status.HTTP_400_BAD_REQUEST)

            product = ProductService.get_product_by_id(product_id)
            if not product:
                return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

            serializer = ProductSerializer(product, data=request.data, partial=True)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            updated_product = ProductService.update_product(product_id, serializer.validated_data)
            return Response(ProductSerializer(updated_product).data, status=status.HTTP_200_OK)

        except (ValidationError, NotUniqueError, ValueError) as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, product_id):
        """Delete a product."""
        try:
            if not ObjectId.is_valid(product_id):
                return Response({"error": "Invalid product ID."}, status=status.HTTP_400_BAD_REQUEST)

            deleted = ProductService.delete_product(product_id)
            if deleted:
                return Response({"message": "Product deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
            
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
