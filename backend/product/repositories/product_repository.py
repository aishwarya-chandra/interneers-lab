# accessing data from MongoDB using MongoEngine ORM
from product.models import Product
from mongoengine import DoesNotExist
from bson import ObjectId
from datetime import datetime

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
    def get_all_paginated(page, page_size, sort_by=None, order='asc'):
        """Fetch paginated and sorted products from MongoDB."""
        skip = (page - 1) * page_size
        sort_order = 1 if order == 'asc' else -1  # 1 for ascending, -1 for descending
        
        # If sort_by is provided, sort by that field
        if sort_by:
            queryset = Product.objects.skip(skip).limit(page_size).order_by(f"{'-' if order == 'desc' else ''}{sort_by}")
        else:
            queryset = Product.objects.skip(skip).limit(page_size)
        
        total_count = Product.objects.count()
        return list(queryset), total_count

    @staticmethod
    def get_by_id(product_id):
        """Fetch a product by ID from MongoDB."""
        try:
            # Convert product_id to ObjectId if it's a string
            if isinstance(product_id, str):
                product_id = ObjectId(product_id)

            return Product.objects(id=product_id).first()
        
        except DoesNotExist:
            return None
        except Exception as e:
            raise ValueError(f"Error fetching product: {str(e)}")
        
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
            update_data['updated_at'] = datetime.utcnow()  # Ensure 'updated_at' gets set
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
