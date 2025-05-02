from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from product.services.product_category_service import ProductCategoryService
from product.serializers import ProductCategorySerializer
from product.serializers import ProductSerializer
from ..services.product_service import ProductService 

class ProductCategoryController(APIView):
    """Controller layer for handling product category HTTP requests."""

    def get(self, request, category_id=None, products=False):
        """Retrieve all categories, a specific one by ID, or products by category."""

        if products and category_id:
            # Fetch products belonging to the category using the service layer
            products = ProductService.get_product_by_category(category_id)

            if not products:
                return Response({"message": "No products found for this category"}, status=status.HTTP_404_NOT_FOUND)

            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        if category_id:
            category = ProductCategoryService.get_category_by_id(category_id)

            if category:
                serializer = ProductCategorySerializer(category)
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

        categories = ProductCategoryService.get_all_categories()
        serializer = ProductCategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        """Create one or multiple categories."""
        serializer = ProductCategorySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        categories = ProductCategoryService.create_category(serializer.validated_data)

        if categories:
            return Response(ProductCategorySerializer(categories).data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "No new categories inserted (duplicates skipped)"}, status=status.HTTP_200_OK)
    
    def put(self, request, category_id):
        """Update a category."""
        category = ProductCategoryService.get_category_by_id(category_id)

        if not category:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductCategorySerializer(category, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        updated_category = ProductCategoryService.update_category(category_id, serializer.validated_data)

        if updated_category:
            return Response(ProductCategorySerializer(updated_category).data, status=status.HTTP_200_OK)

        return Response({"error": "Failed to update category"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, category_id):
        """Delete a category."""
        deleted = ProductCategoryService.delete_category(category_id)

        if deleted:
            return Response({"message": "Category deleted"}, status=status.HTTP_204_NO_CONTENT)

        return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
