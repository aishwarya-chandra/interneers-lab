from repositories.product_category_repository import ProductCategoryRepository

class ProductCategoryService:
    """Service layer to handle product category operations using the repository."""
    
    product_category_repository = ProductCategoryRepository()

    @staticmethod
    def create_category(data):
        """Creates one or multiple product categories using the repository."""
        ProductCategoryService.validate_category_data(data)
        return ProductCategoryService.product_category_repository.create(data)

    @staticmethod
    def get_category_by_id(category_id):
        """Fetches a category by its ID."""
        return ProductCategoryService.product_category_repository.get_by_name_or_id(category_id)

    @staticmethod
    def get_all_categories():
        """Fetches all product categories."""
        return ProductCategoryService.product_category_repository.get_all()

    @staticmethod
    def update_category(category_id, data):
        """Updates an existing product category using the repository."""
        ProductCategoryService.validate_category_data(data)
        return ProductCategoryService.product_category_repository.update(category_id, data)

    @staticmethod
    def delete_category(category_id):
        """Deletes a product category by ID using the repository."""
        return ProductCategoryService.product_category_repository.delete(category_id)
    
    @staticmethod
    def validate_category_data(data):
        if not data.get('name') or not data['name'].strip():
            raise ValueError("Category name cannot be empty.")
        if not data.get('description') or not data['description'].strip():
            raise ValueError("Category description cannot be empty.")
