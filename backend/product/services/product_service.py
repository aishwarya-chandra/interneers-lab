from product.repositories.product_repository import ProductRepository
from product.repositories.product_category_repository import ProductCategoryRepository
from mongoengine import ValidationError, NotUniqueError, DoesNotExist
from bson import ObjectId, DBRef

class ProductService:
    """Service layer for business logic and validations."""

    # @staticmethod
    # def resolve_category(category_value):
    #     """Resolve category by name, ObjectId, or DBRef."""
    #     if not category_value:
    #         raise ValueError("Category cannot be empty.")

    #     if isinstance(category_value, DBRef):
    #         return category_value.id  
    #     if isinstance(category_value, ObjectId):
    #         return category_value
    #     if isinstance(category_value, str):
    #         category_value = category_value.strip()
    #         if ObjectId.is_valid(category_value):
    #             return ObjectId(category_value)
    #         category = ProductCategoryRepository.get_by_name_or_id(category_value)
    #         if category:
    #             return category.id
    #         raise ValueError(f"Category '{category_value}' not found.")
    #     raise TypeError("Invalid category format. Must be ObjectId, DBRef, or valid string.")
    
    @staticmethod
    def get_all_products():
        return ProductRepository.get_all()

    @staticmethod
    def get_product_by_id(product_id):
        try:
            return ProductRepository.get_by_id(product_id)
        except DoesNotExist:
            return None
    
    @staticmethod
    def get_product_by_category(category_id):
        return ProductRepository.get_by_category(category_id)
    
    @staticmethod
    def find_products_by_name(product_name):
        return ProductRepository.find_by_name(product_name)

    @staticmethod
    def create_product(product_data):
        # product_data['category'] = ProductService.resolve_category(product_data.get('category'))
        ProductService.validate_product_data(product_data)
        existing_products = ProductService.find_products_by_name(product_data['name'])
        if existing_products:
            raise ValueError("A product with this name already exists.")
        try:
            return ProductRepository.create(product_data)
        except (ValidationError, NotUniqueError) as e:
            raise ValueError(f"Failed to create product: {str(e)}")
    
    @staticmethod
    def update_product(product_id, updated_data):
        product = ProductService.get_product_by_id(product_id)
        if not product:
            raise ValueError("Product not found.")
        if not product.brand or product.brand.strip() == "":
            updated_data['brand'] = "Unknown"
        ProductService.validate_product_data(updated_data)
        # if 'category' in updated_data:
        #     updated_data['category'] = ProductService.resolve_category(updated_data['category'])

        # Check for duplicate name (excluding the current product)
        existing_products = ProductService.find_products_by_name(updated_data['name'])
        if existing_products and str(existing_products.id) != str(product_id):
            raise ValueError("A product with this name already exists.")
        try:
            return ProductRepository.update(product_id, updated_data)
        except (ValidationError, NotUniqueError) as e:
            raise ValueError(f"Failed to update product: {str(e)}")
    
    @staticmethod
    def delete_product(product_id):
        product = ProductService.get_product_by_id(product_id)
        if not product:
            raise ValueError("Product not found.")
        try:
            ProductRepository.delete(product_id)
            return True
        except Exception as e:
            raise ValueError(f"Failed to delete product: {str(e)}")
    
    @staticmethod
    def validate_product_data(data):
        if not data.get('name') or not data['name'].strip():
            raise ValueError("Product name cannot be empty.")
        if not data.get('description') or not data['description'].strip():
            raise ValueError("Product description cannot be empty.")
        if not data.get('category') or (isinstance(data['category'], str) and not data['category'].strip()):
            raise ValueError("Product category cannot be empty.")
        if not data.get('brand') or not data['brand'].strip():
            raise ValueError("Product brand cannot be empty.")
        try:
            price = float(data['price'])
            if price <= 0:
                raise ValueError("Price must be greater than 0.")
        except (ValueError, TypeError):
            raise ValueError("Price must be a valid number (float).")
        try:
            quantity = int(data['quantity'])
            if quantity < 0:
                raise ValueError("Quantity must be 0 or greater.")
        except (ValueError, TypeError):
            raise ValueError("Quantity must be a valid integer.")
