from product.repositories.product_repository import ProductRepository
from mongoengine import ValidationError, NotUniqueError, DoesNotExist
from datetime import datetime

class ProductService:
    """Service layer for business logic and validations."""
    
    product_repository = ProductRepository()  # Instantiate the repository

    @staticmethod
    def get_all_products(page=1, page_size=10, sort_by=None, order='asc'):
        return ProductService.product_repository.get_all_paginated(page, page_size, sort_by, order)

    @staticmethod
    def get_product_by_id(product_id):
        try:
            return ProductService.product_repository.get_by_id(product_id)
        except DoesNotExist:
            return None
    
    @staticmethod
    def get_product_by_category(category_id):
        return ProductService.product_repository.get_by_category(category_id)
    
    @staticmethod
    def find_products_by_name(product_name):
        return ProductService.product_repository.find_by_name(product_name)

    @staticmethod
    def create_product(product_data):
        ProductService.validate_product_data(product_data)
        existing_products = ProductService.find_products_by_name(product_data['name'])
        if existing_products:
            raise ValueError("A product with this name already exists.")
        try:
            product = ProductService.product_repository.create(product_data)
            product.save()  # This will ensure created_at and updated_at are set correctly by MongoEngine
            return product
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
        existing_products = ProductService.find_products_by_name(updated_data['name'])
        if existing_products and str(existing_products.id) != str(product_id):
            raise ValueError("A product with this name already exists.")
        try:
            for key, value in updated_data.items():
                setattr(product, key, value)
            product.updated_at = datetime.utcnow()  # Manually updating updated_at if needed
            product.save()  # This will update both created_at (if it's new) and updated_at
            return product
        except (ValidationError, NotUniqueError) as e:
            raise ValueError(f"Failed to update product: {str(e)}")
    
    @staticmethod
    def delete_product(product_id):
        product = ProductService.get_product_by_id(product_id)
        if not product:
            raise ValueError("Product not found.")
        try:
            ProductService.product_repository.delete(product_id)
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
