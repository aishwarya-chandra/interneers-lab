from decimal import Decimal 
from mongoengine import Document, StringField, DecimalField, IntField, ReferenceField, CASCADE

class ProductCategory(Document):
    """MongoDB model for product categories using MongoEngine ORM."""
    
    name = StringField(max_length=100, required=True, unique=True)
    description = StringField()

    meta = {'collection': 'product_categories'}  # Collection name in MongoDB

    def __str__(self):
        return self.name


class Product(Document):
    """MongoDB model for products using MongoEngine ORM."""
    
    name = StringField(max_length=255, required=True, unique=True)
    description = StringField(required=True)
    
    # Reference to ProductCategory
    category = ReferenceField(ProductCategory, reverse_delete_rule=CASCADE, required=True)
    
    price = DecimalField(min_value=Decimal("0.01"), precision=2, required=True)
    brand = StringField(max_length=100, required=True)
    quantity = IntField(min_value=1, required=True)

    meta = {'collection': 'products'}  # Collection name in MongoDB

    def __str__(self):
        return self.name

