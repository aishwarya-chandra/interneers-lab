import unittest
from unittest.mock import MagicMock
from product.services.product_service import ProductService
from bson import ObjectId

class TestProductService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mock_repo = MagicMock()
        ProductService.product_repository = cls.mock_repo
    
    def setUp(self):
        self.mock_repo.reset_mock()
        ProductService.product_repository = self.mock_repo

    def test_get_all_products(self):
        valid_id = ObjectId()
        self.mock_repo.get_all.return_value = [{"id": valid_id, "name": "Laptop"}]
        products = ProductService.get_all_products()
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0]["name"], "Laptop")
        self.mock_repo.get_all.assert_called_once()

    def test_get_product_by_id_valid(self):
        valid_id = ObjectId()
        self.mock_repo.get_by_id.return_value = {"id": valid_id, "name": "Laptop"}
        product = ProductService.get_product_by_id(valid_id)
        self.assertEqual(product["name"], "Laptop")
        self.mock_repo.get_by_id.assert_called_once_with(valid_id)

    def test_get_product_by_id_invalid(self):
        invalid_id = ObjectId()
        self.mock_repo.get_by_id.return_value = None
        product = ProductService.get_product_by_id(invalid_id)
        self.assertIs(product, None)
        self.mock_repo.get_by_id.assert_called_once_with(invalid_id)

    def test_get_product_by_category(self):
        valid_id = ObjectId()
        self.mock_repo.get_by_category.return_value = [{"id": valid_id, "name": "Phone"}]
        products = ProductService.get_product_by_category("electronics")
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0]["name"], "Phone")
        self.mock_repo.get_by_category.assert_called_once_with("electronics")

    def test_find_products_by_name(self):
        self.mock_repo.find_by_name.return_value = {"name": "Tablet"}
        product = ProductService.find_products_by_name("Tablet")
        self.assertEqual(product["name"], "Tablet")
        self.mock_repo.find_by_name.assert_called_once_with("Tablet")

    def test_create_product_successful(self):
        self.mock_repo.find_by_name.return_value = None
        valid_id = ObjectId()
        self.mock_repo.create.return_value = {"id": valid_id, "name": "Tablet"}
        product_data = {"name": "Tablet","description": "For educational purposes", "price": 500, "category": "electronics", "brand": "Apple", "quantity": 10}
        product = ProductService.create_product(product_data)
        self.assertEqual(product["name"], "Tablet")
        self.mock_repo.create.assert_called_once()

    def test_create_product_invalid(self):
        invalid_product_data = {
            "name": "",  # Invalid: empty name
            "price": -10,  # Invalid: negative price
            "description": "Laptop with Graphic cards",
            "brand": "Dell",
            "quantity": 5,
            "category": "category_id"
        }
        with self.assertRaises(ValueError) as context:
            ProductService.create_product(invalid_product_data)
        self.assertEqual(str(context.exception), "Product name cannot be empty.")
        invalid_product_data["name"] = "Laptop"
        invalid_product_data["price"] = "invalid_price" 
        with self.assertRaises(ValueError) as context:
            ProductService.create_product(invalid_product_data)
        self.assertEqual(str(context.exception), "Price must be a valid number (float).")

    def test_create_product_duplicate_name(self):
        valid_id = ObjectId()
        self.mock_repo.find_by_name.return_value = {"id": valid_id, "name": "Laptop"}
        with self.assertRaises(ValueError) as context:
            ProductService.create_product({"name": "Laptop", "price": 1000, "description": "Laptop with Graphic cards", "category": "electronics", "brand": "Dell", "quantity": 5})
        self.assertEqual(str(context.exception), "A product with this name already exists.")
        self.mock_repo.create.assert_not_called()

    def test_update_product_successful(self):
        valid_id = ObjectId()
        mock_product = MagicMock()
        mock_product.id = valid_id
        mock_product.name = "Laptop"
        mock_product.brand = "HP"
        self.mock_repo.get_by_id.return_value = mock_product
        self.mock_repo.find_by_name.return_value = None
        self.mock_repo.update.return_value = {"id": valid_id, "name": "Gaming Laptop", "brand": "HP", "description": "Laptop with Graphic cards", "category": "Electronics", "price": "5000", "quantity": 30}
        updated_product = ProductService.update_product(valid_id, {"name": "Gaming Laptop", "brand": "HP",  "description": "Laptop with Graphic cards", "category": "Electronics", "price": "5000", "quantity": 30})
        self.assertEqual(updated_product["name"], "Gaming Laptop")
        self.mock_repo.update.assert_called_once()

    def test_update_product_not_found(self):
        self.mock_repo.get_by_id.return_value = None 
        with self.assertRaises(ValueError) as context:
            ProductService.update_product("non_existing_id", {"name": "Updated Laptop"})
        self.assertEqual(str(context.exception), "Product not found.")
        self.mock_repo.get_by_id.assert_called_once_with("non_existing_id")

    def test_update_product_duplicate_name(self):
        valid_id = ObjectId()
        duplicate_id = ObjectId()
        mock_product = MagicMock()
        mock_product.id = valid_id
        mock_product.name = "Laptop"
        mock_product.brand = "HP"
        mock_duplicate_product = MagicMock()
        mock_duplicate_product.id = duplicate_id
        mock_duplicate_product.name = "Laptop"
        self.mock_repo.get_by_id.return_value = mock_product  
        self.mock_repo.find_by_name.return_value = mock_duplicate_product  
        with self.assertRaises(ValueError) as context:
            ProductService.update_product(valid_id, {"name": "Laptop", "brand": "HP", "description": "Laptop with Graphic cards", "category": "Electronics", "price": "5000", "quantity": 30})
        self.assertEqual(str(context.exception), "A product with this name already exists.")
        self.mock_repo.update.assert_not_called() 

    def test_delete_product_successful(self):
        valid_id = ObjectId()
        self.mock_repo.get_by_id.return_value = {"id": valid_id, "name": "Laptop"}
        self.mock_repo.delete.return_value = True
        result = ProductService.delete_product(valid_id)
        self.assertTrue(result)
        self.mock_repo.delete.assert_called_once_with(valid_id)

    def test_delete_product_not_found(self):
        valid_id = ObjectId()
        self.mock_repo.get_by_id.return_value = None
        with self.assertRaises(ValueError) as context:
            ProductService.delete_product(valid_id)
        self.assertEqual(str(context.exception), "Product not found.")
        self.mock_repo.delete.assert_not_called()

    def test_validate_product_data_invalid_price(self):
        with self.assertRaises(ValueError) as context:
            ProductService.validate_product_data({"name": "Phone", "price": -100, "description": "128MP camera and 256GB Storage", "quantity": 5, "brand": "Samsung", "category": "electronics"})
        self.assertEqual(str(context.exception), "Price must be a valid number (float).")
    
    def test_validate_product_data_invalid_quantity(self):
        with self.assertRaises(ValueError) as context:
            ProductService.validate_product_data({"name": "Phone", "price": 500, "description": "128MP camera and 256GB Storage", "quantity": -2, "brand": "Samsung", "category": "electronics"})
        self.assertEqual(str(context.exception), "Quantity must be a valid integer.")
    
if __name__ == '__main__':
    unittest.main()
