from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer

class ProductListView(APIView):
    """Handles fetching all products and adding a new product."""

    def get(self, request):
        """Fetch all products from the database."""
        products = Product.objects.all()  # Fetch all products
        serializer = ProductSerializer(products, many=True)  
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Create a new product."""
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Save product to database
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailView(APIView):
    """Handles fetching, updating, and deleting a specific product."""

    def get(self, request, product_id):
        """Fetch a specific product by ID."""
        product = get_object_or_404(Product, id=product_id)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, product_id):
        """Update a product by ID."""
        product = get_object_or_404(Product, id=product_id)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()  # Save updates
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, product_id):
        """Delete a product by ID."""
        product = get_object_or_404(Product, id=product_id)
        product.delete()
        return Response({"message": "Product deleted"}, status=status.HTTP_204_NO_CONTENT)
