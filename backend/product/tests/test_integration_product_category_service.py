import unittest
from mongoengine import connect, disconnect
from product.services.product_category_service import ProductCategoryService
from product.models import ProductCategory
from product.seeds.seed_data import seed
from product.seeds.clear_data import clear
from mongoengine.queryset.queryset import QuerySet

class TestProductCategoryService(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        connect(
        db="product_test_db",
        host="localhost",
        port=27017
    )

    def setUp(self):
        clear()
        seed()

    def tearDown(self):
        clear()

    @classmethod
    def tearDownClass(cls):
        disconnect()

    def test_get_all_categories(self):
        categories = ProductCategoryService.get_all_categories()
        self.assertIsInstance(categories, QuerySet)
        self.assertGreaterEqual(len(categories), 1)

    def test_create_category_success(self):
        data = {
            "name": "Accessories",
            "description": "Mobile accessories"
        }
        category = ProductCategoryService.create_category(data)
        self.assertEqual(category.name, data["name"])
        
    def test_create_category_with_invalid_data(self):
        invalid_data_1 = {
            "name": "",
            "description": "Some category description"
        }
        invalid_data_2 = {
            "name": "New Category",
            "description": ""
        }
        with self.assertRaises(ValueError) as context1:
            ProductCategoryService.create_category(invalid_data_1)
        self.assertIn("Category name cannot be empty", str(context1.exception))

        with self.assertRaises(ValueError) as context2:
            ProductCategoryService.create_category(invalid_data_2)
        self.assertIn("Category description cannot be empty", str(context2.exception))

    def test_update_category_success(self):
        category = ProductCategory.objects.first()
        update_data = {
            "name": "Updated Name",
            "description": "Updated Description"
        }
        updated = ProductCategoryService.update_category(str(category.id), update_data)
        self.assertEqual(updated.name, "Updated Name")
        self.assertEqual(updated.description, "Updated Description")

    def test_update_category_invalid_data(self):
        category = ProductCategory.objects.first()
        update_data = {
            "name": "",
            "description": ""
        }
        with self.assertRaises(ValueError):
            ProductCategoryService.update_category(str(category.id), update_data)

    def test_delete_category_success(self):
        category = ProductCategory.objects.first()
        result = ProductCategoryService.delete_category(str(category.id))
        self.assertTrue(result)

    def test_get_category_by_id_success(self):
        category = ProductCategory.objects.first()
        fetched = ProductCategoryService.get_category_by_id(str(category.id))
        self.assertEqual(fetched.id, category.id)

    def test_get_category_by_id_not_found(self):
        result = ProductCategoryService.get_category_by_id("660d5f5d77a4b79a1a9b8fbb")  # random ObjectId
        self.assertIsNone(result)

