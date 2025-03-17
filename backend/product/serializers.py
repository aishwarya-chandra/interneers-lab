from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'  # Include all fields = ['id', 'name','description', 'category', 'price', 'brand', 'quantity']
