# from mongoengine import ValidationError, NotUniqueError, BulkWriteError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from product.repositories.product_category_repository import ProductCategoryRepository
from product.serializers import ProductCategorySerializer
from product.models import ProductCategory
from ..repositories.product_repository import ProductRepository

class ProductCategoryController(APIView):
    """Controller layer for handling product category HTTP requests using serializers."""

    def get(self, request, category_id=None, products=False):
        """Retrieve all categories, a specific one by ID, or products by category."""

        # Check if fetching products by category
        if products and category_id:
            # Fetch products belonging to the category
            products = ProductRepository.get_by_category(category_id)

            if not products:
                return Response({"message": "No products found for this category"}, status=status.HTTP_404_NOT_FOUND)

            serializer = ProductCategorySerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Fetch specific category
        if category_id:
            category = ProductCategoryRepository.get_by_name_or_id(category_id)

            if category:
                serializer = ProductCategorySerializer(category)
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

        # Fetch all categories
        categories = ProductCategoryRepository.get_all()
        serializer = ProductCategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        """Create one or multiple categories."""
        data = request.data

        if isinstance(data, list):
            serializer = ProductCategorySerializer(data=data, many=True)
        else:
            serializer = ProductCategorySerializer(data=[data], many=True)

        if serializer.is_valid():
            categories_to_insert = []

            # Filter out duplicates using 'name'
            for category_data in serializer.validated_data:
                if not ProductCategory.objects(name=category_data['name']).first():
                    categories_to_insert.append(ProductCategory(**category_data))

            if categories_to_insert:
                ProductCategory.objects.insert(categories_to_insert, load_bulk=False)
                return Response({"message": "Categories inserted successfully"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"message": "No new categories inserted (duplicates skipped)"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, category_id):
        """Update a category."""
        
        category = ProductCategoryRepository.get_by_name_or_id(category_id)
        
        if not category:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductCategorySerializer(category, data=request.data, partial=True)
        
        if serializer.is_valid():
            updated_category = ProductCategoryRepository.update(category_id, serializer.validated_data)
            return Response(ProductCategorySerializer(updated_category).data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, category_id):
        """Delete a category."""
        
        deleted = ProductCategoryRepository.delete(category_id)

        if deleted:
            return Response({"message": "Category deleted"}, status=status.HTTP_204_NO_CONTENT)
        
        return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
