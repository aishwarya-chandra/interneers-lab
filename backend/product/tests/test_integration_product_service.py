import unittest
from product.services.product_service import ProductService
from product.models import Product
from product.models import ProductCategory
from mongoengine import connect, disconnect
from product.seeds.seed_data import seed
from product.seeds.clear_data import clear
from decimal import Decimal
from mongoengine.queryset.queryset import QuerySet

class TestProductServiceIntegration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        disconnect(alias='default')
        connect(
        db="product_test_db",
        host="localhost",
        port=27017
    )

    def setUp(self):
        clear()
        seed()
        # Get a seeded category for linking with products
        self.category = ProductCategory.objects.first()

    def tearDown(self):
        clear()

    def test_create_product_success(self):
        product_data = {
            "name": "Bluetooth Speaker",
            "description": "Portable speaker",
            "category": str(self.category.id),
            "price": Decimal("49.99"),
            "brand": "JBL",
            "quantity": 10
        }
        product = ProductService.create_product(product_data)
        self.assertEqual(product.name, product_data["name"])
        self.assertEqual(product.brand, product_data["brand"])

    def test_create_duplicate_product_should_fail(self):
        product_data = {
            "name": "Tablet", 
            "description": "Android tablet",
            "category": str(self.category.id),
            "price": Decimal("499.99"),
            "brand": "Samsung",
            "quantity": 8
        }
        ProductService.create_product(product_data)
        with self.assertRaises(ValueError) as context:
            ProductService.create_product(product_data)
        self.assertIn("A product with this name already exists.", str(context.exception))

    def test_create_product_missing_name(self):
        invalid_data = {
            "description": "Some description",
            "category": str(self.category.id),
            "price": 10.0,
            "brand": "Brand",
            "quantity": 5
        }
        with self.assertRaises(ValueError) as context:
            ProductService.create_product(invalid_data)
        self.assertIn("Product name cannot be empty", str(context.exception))

    def test_create_product_invalid_price(self):
        invalid_data = {
            "name": "Invalid Price Product",
            "description": "Some description",
            "category": str(self.category.id),
            "price": -10.0,
            "brand": "Brand",
            "quantity": 5
        }
        with self.assertRaises(ValueError) as context:
            ProductService.create_product(invalid_data)
        self.assertIn("Price must be a valid number (float).", str(context.exception))


    def test_get_all_products(self):
        products = ProductService.get_all_products()
        self.assertIsInstance(products, list)
        self.assertGreaterEqual(len(products), 1)

    def test_get_product_by_id_success(self):
        product = ProductService.create_product({
            "name": "Monitor",
            "description": "24 inch HD monitor",
            "category": str(self.category.id),
            "price": Decimal("129.99"),
            "brand": "HP",
            "quantity": 3
        })
        fetched = ProductService.get_product_by_id(str(product.id))
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.name, "Monitor")

    def test_get_product_by_id_not_found(self):
        invalid_id = "642c91fcb80fc7a1a6fbd123"  # Sample MongoDB ObjectId format
        product = ProductService.get_product_by_id(invalid_id)
        self.assertIsNone(product)

    def test_get_product_by_category(self):
        category = ProductCategory.objects.first()
        products = ProductService.get_product_by_category(str(category.id))
        self.assertIsInstance(products, QuerySet)
        self.assertGreaterEqual(len(products), 1)
        for p in products:
            self.assertEqual(p.category.id, category.id)

    def test_get_product_by_category_no_products(self):
        empty_category = ProductCategory(name="EmptyCategory", description="No products here")
        empty_category.save()
        products = ProductService.get_product_by_category(str(empty_category.id))
        self.assertIsInstance(products, QuerySet)
        self.assertEqual(len(products), 0)

    def test_find_products_by_name(self):
        product = Product.objects.first()
        found_products = ProductService.find_products_by_name(product.name)
        self.assertIsInstance(found_products, Product)
        self.assertGreaterEqual(len(found_products), 1)
        self.assertEqual(found_products.name, product.name)

    def test_update_product_success(self):
        product = ProductService.create_product({
            "name": "Keyboard",
            "description": "Mechanical keyboard",
            "category": self.category.id,
            "price": Decimal("79.99"),
            "brand": "Logitech",
            "quantity": 5
        })
        updated = ProductService.update_product(str(product.id), {
            "name": "Keyboard",
            "description": "RGB mechanical keyboard",
            "category": self.category.id,
            "price": Decimal("89.99"),
            "brand": "Logitech",
            "quantity": 8
        })
        self.assertEqual(updated.description, "RGB mechanical keyboard")
        self.assertEqual(updated.quantity, 8)

    def test_update_product_invalid_quantity(self):
        product = Product.objects.first()
        update_data = {
            "name": product.name,
            "description": product.description,
            "category": str(product.category.id),
            "price": float(product.price),
            "brand": product.brand,
            "quantity": -10  # Invalid quantity
        }
        with self.assertRaises(ValueError) as context:
            ProductService.update_product(str(product.id), update_data)
        self.assertIn("Quantity must be a valid integer.", str(context.exception))

    def test_delete_product_success(self):
        product = ProductService.create_product({
            "name": "Mouse",
            "description": "Wireless mouse",
            "category": str(self.category.id),
            "price": Decimal("39.99"),
            "brand": "HP",
            "quantity": 7
        })
        result = ProductService.delete_product(str(product.id))
        self.assertTrue(result)
        self.assertIsNone(ProductService.get_product_by_id(str(product.id)))

    @classmethod
    def tearDownClass(cls):
        disconnect()
