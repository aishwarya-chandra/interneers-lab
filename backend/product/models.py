from mongoengine import Document, StringField, DecimalField, IntField

class Product(Document):
    """MongoDB model for products using MongoEngine ORM."""
    
    name = StringField(max_length=255, required=True, unique=True)
    description = StringField(required=True)
    category = StringField(max_length=100, required=True)
    price = DecimalField(min_value=0.01, precision=2, required=True)
    brand = StringField(max_length=100, required=True)
    quantity = IntField(min_value=1, required=True)

    meta = {'collection': 'products'}  # Collection name in MongoDB

    def __str__(self):
        return self.name
