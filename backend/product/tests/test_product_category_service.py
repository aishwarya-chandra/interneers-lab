import unittest
from unittest.mock import MagicMock
from product.services.product_category_service import ProductCategoryService
from bson import ObjectId

class TestProductCategoryService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mock_repo = MagicMock()
        ProductCategoryService.product_category_repository = cls.mock_repo
    
    def setUp(self):
        self.mock_repo.reset_mock()
        self.mock_repo.create.side_effect = None
        ProductCategoryService.product_category_repository = self.mock_repo

    def test_create_category_successful(self):
        category_data = {"name": "Electronics", "description": "Devices and gadgets"}
        self.mock_repo.create.return_value = category_data
        result = ProductCategoryService.create_category(category_data)
        self.assertEqual(result, category_data)
        self.mock_repo.create.assert_called_once_with(category_data)
    
    def test_create_category_duplicate(self):
        category_data = {"name": "Electronics", "description": "Devices and gadgets"}
        self.mock_repo.create.side_effect = ValueError("Category 'Electronics' already exists.")
        with self.assertRaises(ValueError) as context:
            ProductCategoryService.create_category(category_data)
        self.assertEqual(str(context.exception), "Category 'Electronics' already exists.")
    
    def test_create_category_invalid_data(self):
        invalid_data = {"name": "", "description": ""}  
        with self.assertRaises(ValueError) as context:
            ProductCategoryService.create_category(invalid_data)
        self.assertEqual(str(context.exception), "Category name cannot be empty.")
    
    def test_get_category_by_id_successful(self):
        category_id = ObjectId()
        category = {"id": category_id, "name": "Electronics"}
        self.mock_repo.get_by_name_or_id.return_value = category
        result = ProductCategoryService.get_category_by_id(category_id)
        self.assertEqual(result, category)
        self.mock_repo.get_by_name_or_id.assert_called_once_with(category_id)
    
    def test_get_category_by_id_not_found(self):
        category_id = ObjectId()
        self.mock_repo.get_by_name_or_id.return_value = None
        result = ProductCategoryService.get_category_by_id(category_id)
        self.assertIsNone(result)
    
    def test_get_all_categories(self):
        categories = [{"name": "Electronics"}, {"name": "Clothing"}]
        self.mock_repo.get_all.return_value = categories
        result = ProductCategoryService.get_all_categories()
        self.assertEqual(result, categories)
        self.mock_repo.get_all.assert_called_once()
    
    def test_update_category_successful(self):
        category_id = ObjectId()
        updated_data = {"name": "Updated Electronics", "description": "Gadets and Wearables"}
        self.mock_repo.update.return_value = updated_data
        result = ProductCategoryService.update_category(category_id, updated_data)
        self.assertEqual(result, updated_data)
        self.mock_repo.update.assert_called_once_with(category_id, updated_data)
    
    def test_update_category_not_found(self):
        category_id = ObjectId()
        self.mock_repo.update.return_value = None
        result = ProductCategoryService.update_category(category_id, {"name": "Updated Electronics", "description": "Gadets and Wearables"})
        self.assertIsNone(result)
    
    def test_update_category_invalid_data(self):
        category_id = ObjectId()
        invalid_data = {"name": ""}  # Invalid name
        with self.assertRaises(ValueError) as context:
            ProductCategoryService.update_category(category_id, invalid_data)
        self.assertEqual(str(context.exception), "Category name cannot be empty.")
    
    def test_delete_category_successful(self):
        category_id = ObjectId()
        self.mock_repo.delete.return_value = True
        result = ProductCategoryService.delete_category(category_id)
        self.assertTrue(result)
        self.mock_repo.delete.assert_called_once_with(category_id)
    
    def test_delete_category_not_found(self):
        category_id = ObjectId()
        self.mock_repo.delete.return_value = False
        result = ProductCategoryService.delete_category(category_id)
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
        