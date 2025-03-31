# accessing data from MongoDB using MongoEngine ORM
from product.models import Product
from mongoengine import DoesNotExist

class ProductRepository:
    """Repository layer for interacting with MongoDB using MongoEngine."""

    @staticmethod
    def create(product_data):
        """Create a new product in MongoDB."""
        try:
            product = Product(**product_data)
            product.save()
            return product
        except Exception as e:
            raise ValueError(f"Error creating product: {str(e)}")

    @staticmethod
    def get_all():
        """Fetch all products from MongoDB."""
        return Product.objects.select_related()  # Dereference the category

    @staticmethod
    def get_by_id(product_id):
        """Fetch a product by ID from MongoDB."""
        try:
            return Product.objects(id=product_id).select_related('category').first()
        except DoesNotExist:
            return None
        
    @staticmethod
    def get_by_category(category_id):
        """Fetch all products belonging to a specific category."""
        return Product.objects(category=category_id)

    @staticmethod
    def find_by_name(name):
        """Check if a product with the given name already exists."""
        return Product.objects(name=name).first()

    @staticmethod
    def update(product_id, update_data):
        """Update a product by ID in MongoDB."""
        try:
            product = Product.objects.get(id=product_id)
            product.update(**update_data)
            return Product.objects.get(id=product_id)  # Return the updated product
        except DoesNotExist:
            return None
        except Exception as e:
            raise ValueError(f"Error updating product: {str(e)}")

    @staticmethod
    def delete(product_id):
        """Delete a product by ID in MongoDB."""
        try:
            product = Product.objects.get(id=product_id)
            product.delete()
            return True
        except DoesNotExist:
            return False
        except Exception as e:
            raise ValueError(f"Error deleting product: {str(e)}")
