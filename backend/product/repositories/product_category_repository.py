from ..models import ProductCategory
from mongoengine import DoesNotExist, ValidationError, NotUniqueError

class ProductCategoryRepository:
    """Repository layer to handle product category database operations."""

    @staticmethod
    def create(data):
        """Create a new product category."""
        try:
            category = ProductCategory(**data)
            category.save()
            return category
        except NotUniqueError:
            raise ValueError("Category with this title already exists.")
        except ValidationError as e:
            raise ValueError(str(e))

    @staticmethod
    def get_by_id(category_id):
        """Fetch a product category by ID."""
        try:
            return ProductCategory.objects.get(id=category_id)
        except DoesNotExist:
            return None

    @staticmethod
    def get_all():
        """Retrieve all product categories."""
        return ProductCategory.objects.all()

    @staticmethod
    def update(category_id, data):
        """Update an existing category."""
        category = ProductCategoryRepository.get_by_id(category_id)

        if not category:
            return None

        # Update only provided fields
        if 'title' in data:
            category.title = data['title']
        if 'description' in data:
            category.description = data['description']

        category.save()
        return category

    @staticmethod
    def delete(category_id):
        """Delete a product category."""
        category = ProductCategoryRepository.get_by_id(category_id)

        if not category:
            return False

        category.delete()
        return True
