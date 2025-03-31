from rest_framework_mongoengine.serializers import DocumentSerializer
from product.models import Product, ProductCategory
from rest_framework import serializers

class ProductSerializer(DocumentSerializer):
    """Serializer for MongoEngine Product model"""
    
    class Meta:
        model = Product
        fields = '__all__'

class ProductCategorySerializer(DocumentSerializer):
    """Serializer for MongoEngine ProductCategory model."""

    class Meta:
        model = ProductCategory
        fields = '__all__'

    def validate_name(self, value):
        """Ensure name is not null or empty."""
        if not value:
            raise serializers.ValidationError("Name cannot be null or empty.")
        return value

    def to_internal_value(self, data):
        """Handle both single and bulk insertion."""
        if isinstance(data, list):
            return [super(ProductCategorySerializer, self).to_internal_value(item) for item in data]
        return super(ProductCategorySerializer, self).to_internal_value(data)