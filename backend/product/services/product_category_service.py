from ..models import ProductCategory
from mongoengine import DoesNotExist, ValidationError, NotUniqueError

class ProductCategoryService:
    """Service layer to handle product category operations."""

    @staticmethod
    def create_category(data):
        """Creates one or multiple product categories."""
        if isinstance(data, list):  # Check if it's a list
            categories = []
            for category_data in data:
                if isinstance(category_data, dict):
                    try:
                        category = ProductCategory(**category_data)
                        category.save()
                        categories.append(category)
                    except NotUniqueError:
                        raise ValueError(f"Category '{category_data['name']}' already exists.")
                    except ValidationError as e:
                        raise ValueError(str(e))
            return categories
        else:  # Single category
            try:
                category = ProductCategory(**data)
                category.save()
                return category
            except NotUniqueError:
                raise ValueError("Category with this name already exists.")
            except ValidationError as e:
                raise ValueError(str(e))

    @staticmethod
    def get_category_by_id(category_id):
        """Fetches a category by its ID."""
        try:
            return ProductCategory.objects.get(id=category_id)
        except DoesNotExist:
            return None

    @staticmethod
    def get_all_categories():
        """Fetches all product categories."""
        return ProductCategory.objects.all()

    @staticmethod
    def update_category(category_id, data):
        """Updates an existing product category."""
        category = ProductCategoryService.get_category_by_id(category_id)
        
        if not category:
            return None

        # Update only the provided fields
        if 'name' in data:
            category.name = data['name']
        if 'description' in data:
            category.description = data['description']

        category.save()
        return category

    @staticmethod
    def delete_category(category_id):
        """Deletes a product category by ID."""
        category = ProductCategoryService.get_category_by_id(category_id)
        
        if not category:
            return False
        
        category.delete()
        return True
