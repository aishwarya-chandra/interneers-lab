from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255, required=True)
    description = serializers.CharField(required=True)
    category = serializers.CharField(max_length=100, required=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0.01)  # Price must be > 0
    brand = serializers.CharField(max_length=100, required=True)
    quantity = serializers.IntegerField(min_value=1)  # Quantity must be ≥ 1

    class Meta:
        model = Product
        fields = '__all__'  # Include all fields = ['id', 'name','description', 'category', 'price', 'brand', 'quantity']

    def validate_name(self, value):
        """Ensure product name is unique and not empty."""
        if not value.strip():
            raise serializers.ValidationError("Product name cannot be empty.")

        # Exclude the current product during updates
        if self.instance:  # Check if updating an existing product
            if Product.objects.filter(name=value).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError("A product with this name already exists.")
        else:  # Creating a new product
            if Product.objects.filter(name=value).exists():
                raise serializers.ValidationError("A product with this name already exists.")

        return value


    def validate_category(self, value):
        """Ensure category is not empty."""
        if not value.strip():
            raise serializers.ValidationError("Category cannot be empty.")
        return value

    def validate_brand(self, value):
        """Ensure brand is not empty."""
        if not value.strip():
            raise serializers.ValidationError("Brand cannot be empty.")
        return value
