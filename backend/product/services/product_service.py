# handles business logic and validations along with error handling
from product.repositories.product_repository import ProductRepository
from mongoengine import ValidationError, NotUniqueError

class ProductService:
    """Service layer for business logic and validations."""

    @staticmethod
    def get_all_products():
        """Business logic to fetch all products."""
        return ProductRepository.get_all()

    @staticmethod
    def get_product_by_id(product_id):
        """Business logic to get a product by ID."""
        return ProductRepository.get_by_id(product_id)

    @staticmethod
    def create_product(product_data):
        """Business logic for creating a product with validation."""
        
        # Validate product data
        ProductService.validate_product_data(product_data)

        # Check for duplicate name
        if ProductRepository.find_by_name(product_data['name']):
            raise ValueError("A product with this name already exists.")
        
        try:
            return ProductRepository.create(product_data)
        except (ValidationError, NotUniqueError) as e:
            raise ValueError(f"Failed to create product: {str(e)}")

    @staticmethod
    def update_product(product_id, updated_data):
        """Business logic for updating a product."""
        
        # Check if the product exists
        product = ProductRepository.get_by_id(product_id)
        if not product:
            return None

        # Validate the updated product data
        ProductService.validate_product_data(updated_data)

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
        """Business logic for deleting a product."""
        
        # Check if the product exists
        product = ProductRepository.get_by_id(product_id)
        if product:
            try:
                ProductRepository.delete(product_id)  # Pass ID, not object
                return True
            except Exception as e:
                raise ValueError(f"Failed to delete product: {str(e)}")
        return False

    @staticmethod
    def validate_product_data(data):
        """Reusable validation logic for product creation and update."""
        
        # Required field validations
        if not data.get('name') or not data['name'].strip():
            raise ValueError("Product name cannot be empty.")
        if not data.get('description') or not data['description'].strip():
            raise ValueError("Product description cannot be empty.")
        if not data.get('category') or not data['category'].strip():
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
            if quantity <= 0:
                raise ValueError("Quantity must be greater than 0.")
        except (ValueError, TypeError):
            raise ValueError("Quantity must be a valid integer.")
