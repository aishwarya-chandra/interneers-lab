from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from product.repositories.product_category_repository import ProductCategoryRepository
from mongoengine import ValidationError, NotUniqueError

class ProductCategoryController(APIView):
    """Controller layer for handling product category HTTP requests."""

    def get(self, request, category_id=None):
        """Retrieve all categories or a specific one by ID."""
        if category_id:
            # Fetch a specific category
            category = ProductCategoryRepository.get_by_id(category_id)
            
            if category:
                return Response(category.to_mongo().to_dict(), status=status.HTTP_200_OK)
            
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Fetch all categories
        categories = ProductCategoryRepository.get_all()
        category_list = [c.to_mongo().to_dict() for c in categories]

        return Response(category_list, status=status.HTTP_200_OK)

    def post(self, request):
        """Create a new category."""
        try:
            category = ProductCategoryRepository.create(request.data)
            return Response(category.to_mongo().to_dict(), status=status.HTTP_201_CREATED)

        except (ValueError, ValidationError, NotUniqueError) as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, category_id):
        """Update a category."""
        try:
            updated_category = ProductCategoryRepository.update(category_id, request.data)

            if updated_category:
                return Response(updated_category.to_mongo().to_dict(), status=status.HTTP_200_OK)
            
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

        except (ValueError, ValidationError) as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, category_id):
        """Delete a category."""
        deleted = ProductCategoryRepository.delete(category_id)

        if deleted:
            return Response({"message": "Category deleted"}, status=status.HTTP_204_NO_CONTENT)
        
        return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
