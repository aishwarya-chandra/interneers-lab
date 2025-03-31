# handles business logic and validations along with error handling
from product.repositories.product_repository import ProductRepository
from product.repositories.product_category_repository import ProductCategoryRepository
from mongoengine import ValidationError, NotUniqueError, DoesNotExist
from bson import ObjectId, DBRef
class ProductService:
    """Service layer for business logic and validations."""

    @staticmethod
    def resolve_category(category_value):
        """Resolve category by name, ObjectId, or DBRef."""
        if not category_value:
            raise ValueError("Category cannot be empty.")

        # Handle DBRef extraction
        if isinstance(category_value, DBRef):
            return category_value.id  # Extract ObjectId from DBRef
        
        # If already ObjectId, return it directly
        if isinstance(category_value, ObjectId):
            return category_value
        
        # Handle string input (either ObjectId or category name)
        if isinstance(category_value, str):
            category_value = category_value.strip()

            # Check if valid ObjectId string
            if ObjectId.is_valid(category_value):
                return ObjectId(category_value)

            # Fetch by category name if not ObjectId
            from product.repositories.product_category_repository import ProductCategoryRepository
            category = ProductCategoryRepository.get_by_name_or_id(category_value)
            
            if category:
                return category.id
            else:
                raise ValueError(f"Category '{category_value}' not found.")
        
        # Raise error for invalid format
        raise TypeError("Invalid category format. Must be ObjectId, DBRef, or valid string.")

    @staticmethod
    def get_all_products():
        """Fetch all products."""
        return ProductRepository.get_all()
    
    @staticmethod
    def get_category_object_id(category_value):
        """Convert category name or ObjectId to ObjectId."""
        if not category_value:
            raise ValueError("Category cannot be empty.")

        if isinstance(category_value, str):
            category_value = category_value.strip()

            if ObjectId.is_valid(category_value):
                return ObjectId(category_value)  # Use ObjectId directly if valid
            else:
                # Fetch by category name if not an ObjectId
                category = ProductCategoryRepository.get_by_name_or_id(category_value)

                if category:
                    # Ensure you return the raw ObjectId, not DBRef
                    if isinstance(category.id, DBRef):
                        return category.id.id  # Extract the ObjectId from DBRef
                    return category.id
                else:
                    raise ValueError(f"Category '{category_value}' not found.")
                
        elif isinstance(category_value, DBRef):
            # Extract ObjectId from DBRef
            return category_value.id       
         
        else:
            raise TypeError("Invalid category format. Must be a string or ObjectId.")


    @staticmethod
    def get_product_by_id(product_id):
        """Get a product by ID."""
        return ProductRepository.get_by_id(product_id)

    @staticmethod
    def create_product(product_data):
        """Create a product with validation."""

        # Validate product data
        ProductService.validate_product_data(product_data)

        # Resolve and assign category ID
        category_value = product_data.get('category')
        product_data['category'] = ProductService.resolve_category(category_value)

        # Check for duplicate product name
        if ProductRepository.find_by_name(product_data['name']):
            raise ValueError("A product with this name already exists.")

        try:
            return ProductRepository.create(product_data)
        except (ValidationError, NotUniqueError) as e:
            raise ValueError(f"Failed to create product: {str(e)}")

    @staticmethod
    def update_product(product_id, updated_data):
        """Update a product."""

        # Check if the product exists
        product = ProductRepository.get_by_id(product_id)
        if not product:
            raise ValueError("Product not found.")

        # Validate the updated data
        ProductService.validate_product_data(updated_data)

        # Resolve and assign the category ID
        if 'category' in updated_data:
            updated_data['category'] = ProductService.resolve_category(updated_data['category'])

        # Check for duplicate name (excluding the current product)
        existing_product = ProductRepository.find_by_name(updated_data['name'])
        if existing_product and str(existing_product.id) != str(product_id):
            raise ValueError("A product with this name already exists.")

        try:
            return ProductRepository.update(product_id, updated_data)
        except (ValidationError, NotUniqueError) as e:
            raise ValueError(f"Failed to update product: {str(e)}")

    @staticmethod
    def delete_product(product_id):
        """Delete a product."""

        product = ProductRepository.get_by_id(product_id)
        if not product:
            raise ValueError("Product not found.")

        try:
            ProductRepository.delete(product_id)
            return True
        except Exception as e:
            raise ValueError(f"Failed to delete product: {str(e)}")

    @staticmethod
    def validate_product_data(data):
        """Reusable validation logic for product creation and update."""

        # Required field validations
        if not data.get('name') or not data['name'].strip():
            raise ValueError("Product name cannot be empty.")
        if not data.get('description') or not data['description'].strip():
            raise ValueError("Product description cannot be empty.")
        if not data.get('category') or (isinstance(data['category'], str) and not data['category'].strip()):
            raise ValueError("Product category cannot be empty.")
        if not data.get('brand') or not data['brand'].strip():
            raise ValueError("Product brand cannot be empty.")

        # Price validation
        try:
            price = float(data['price'])
            if price <= 0:
                raise ValueError("Price must be greater than 0.")
        except (ValueError, TypeError):
            raise ValueError("Price must be a valid number (float).")

        # Quantity validation
        try:
            quantity = int(data['quantity'])
            if quantity < 0:
                raise ValueError("Quantity must be 0 or greater.")
        except (ValueError, TypeError):
            raise ValueError("Quantity must be a valid integer.")
