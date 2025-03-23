from rest_framework_mongoengine.serializers import DocumentSerializer
from product.models import Product

class ProductSerializer(DocumentSerializer):
    """Serializer for MongoEngine Product model"""
    
    class Meta:
        model = Product
        fields = '__all__'
