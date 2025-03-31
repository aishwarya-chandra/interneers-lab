from ..models import ProductCategory
from mongoengine import ValidationError, NotUniqueError
from bson import ObjectId

class ProductCategoryRepository:
    """Repository layer to handle product category database operations."""

    @staticmethod
    def create(data):
        """Create a single or multiple product categories."""
        try:
            if isinstance(data, list):  # Bulk insertion
                categories = [ProductCategory(**item) for item in data]
                
                # Check for duplicates in bulk
                for category_data in data:
                    if ProductCategory.objects(name=category_data['name']).first():
                        raise ValueError(f"Category '{category_data['name']}' already exists.")
                
                ProductCategory.objects.insert(categories, load_bulk=False)
                return categories
            
            elif isinstance(data, dict):  # Single insertion
                if ProductCategory.objects(name=data['name']).first():
                    raise ValueError(f"Category '{data['name']}' already exists.")
                
                category = ProductCategory(**data)
                category.save()
                return category

            else:
                raise ValueError("Invalid data format. Expected dictionary or list.")

        except NotUniqueError:
            raise ValueError("One or more categories already exist.")
        except ValidationError as e:
            raise ValueError(str(e))
        
    @staticmethod
    def get_by_name_or_id(value):
        """Retrieve a ProductCategory by name or ObjectId."""
        if ObjectId.is_valid(value):
            # Search by ObjectId
            return ProductCategory.objects(id=value).first()
        else:
            # Search by category name
            return ProductCategory.objects(name=value).first()

    @staticmethod
    def get_all():
        """Retrieve all product categories."""
        return ProductCategory.objects.all()

    @staticmethod
    def update(category_id, data):
        """Update an existing category."""
        category = ProductCategoryRepository.get_by_name_or_id(category_id)

        if not category:
            return None

       # Apply partial updates only for provided fields
        for key, value in data.items():
            setattr(category, key, value)

        category.save()
        return category

    @staticmethod
    def delete(category_id):
        """Delete a product category."""
        category = ProductCategoryRepository.get_by_name_or_id(category_id)

        if not category:
            return False

        category.delete()
        return True
