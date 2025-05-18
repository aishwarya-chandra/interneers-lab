from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from product.services.product_service import ProductService
from product.serializers import ProductSerializer
from mongoengine import DoesNotExist, ValidationError, NotUniqueError
from bson import ObjectId
import pytz
from datetime import datetime

# Function to convert UTC to IST
def convert_utc_to_ist(utc_time):
    kolkata_timezone = pytz.timezone('Asia/Kolkata')
    # Ensure the datetime is in UTC before conversion
    utc_time = utc_time.replace(tzinfo=pytz.utc)
    # Convert to IST
    return utc_time.astimezone(kolkata_timezone)

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
                    # Convert timestamps to IST before returning
                    created_at_ist = convert_utc_to_ist(product.created_at).strftime("%Y-%m-%d %H:%M:%S")
                    updated_at_ist = convert_utc_to_ist(product.updated_at).strftime("%Y-%m-%d %H:%M:%S")
                    data = ProductSerializer(product).data
                    data["created_at"] = created_at_ist
                    data["updated_at"] = updated_at_ist
                    return Response(data, status=status.HTTP_200_OK)
                return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

            # Handle pagination parameters
            page = int(request.GET.get("page", 1))
            page_size = int(request.GET.get("page_size", 5))

            # Fetch paginated products and metadata
            products, total_count = ProductService.get_all_products(page=page, page_size=page_size)
            total_pages = (total_count + page_size - 1) // page_size

            # Convert timestamps for each product to IST
            products_data = []
            for product in products:
                product_data = ProductSerializer(product).data
                product_data["created_at"] = convert_utc_to_ist(product.created_at).strftime("%Y-%m-%d %H:%M:%S")
                product_data["updated_at"] = convert_utc_to_ist(product.updated_at).strftime("%Y-%m-%d %H:%M:%S")
                products_data.append(product_data)

            return Response({
                "count": total_count,
                "next": f"{request.build_absolute_uri(request.path)}?page={page + 1}" if (page * page_size) < total_count else None,
                "previous": f"{request.build_absolute_uri(request.path)}?page={page - 1}" if page > 1 else None,
                "results": products_data
            }, status=status.HTTP_200_OK)

        except (ValidationError, DoesNotExist, ValueError) as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        """Create a new product."""
        try:
            serializer = ProductSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            product = ProductService.create_product(serializer.validated_data)
            # Convert timestamps to IST before returning
            created_at_ist = convert_utc_to_ist(product.created_at).strftime("%Y-%m-%d %H:%M:%S")
            updated_at_ist = convert_utc_to_ist(product.updated_at).strftime("%Y-%m-%d %H:%M:%S")
            data = ProductSerializer(product).data
            data["created_at"] = created_at_ist
            data["updated_at"] = updated_at_ist
            return Response(data, status=status.HTTP_201_CREATED)

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

            # Remove created_at from the data being passed for update
            if 'created_at' in serializer.validated_data:
                del serializer.validated_data['created_at']

            updated_product = ProductService.update_product(product_id, serializer.validated_data)

            # Convert timestamps to IST before returning
            created_at_ist = convert_utc_to_ist(updated_product.created_at).strftime("%Y-%m-%d %H:%M:%S")
            updated_at_ist = convert_utc_to_ist(updated_product.updated_at).strftime("%Y-%m-%d %H:%M:%S")
            data = ProductSerializer(updated_product).data
            data["created_at"] = created_at_ist
            data["updated_at"] = updated_at_ist
            return Response(data, status=status.HTTP_200_OK)

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
