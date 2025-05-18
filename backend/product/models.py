from decimal import Decimal 
from datetime import datetime
from mongoengine import Document, StringField, DecimalField, IntField, ReferenceField, DateTimeField, CASCADE

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
    category = ReferenceField(ProductCategory, reverse_delete_rule=CASCADE, required=True, dbref=False, store_as_ref=False)
    
    price = DecimalField(min_value=Decimal("0.01"), precision=2, required=True)
    brand = StringField(max_length=100, required=True)
    quantity = IntField(min_value=1, required=True)

    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {'collection': 'products'}  # Collection name in MongoDB

    def save(self, *args, **kwargs):
        """Auto-update the updated_at timestamp on every save and preserve created_at."""
        if not self.created_at:
            self.created_at = datetime.utcnow()  # Set created_at only if it is None
        self.updated_at = datetime.utcnow()  # Always update updated_at on save
        return super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


