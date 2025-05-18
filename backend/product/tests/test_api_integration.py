from django.test import SimpleTestCase, Client
from mongoengine import connect, disconnect
from product.seeds.seed_data import seed
from product.seeds.clear_data import clear
from product.models import Product, ProductCategory
import json

class ProductAPIIntegrationTest(SimpleTestCase):
    @classmethod
    def setUpClass(cls):
        disconnect(alias='default')
        connect(
        db="product_test_db",
        host="localhost",
        port=27017
    )
        
    def setUp(self):
        self.client = Client()
        self.seeded_data = seed() 

    def tearDown(self):
        clear()

    @classmethod
    def tearDownClass(cls):
        disconnect()

    # GET
    def test_get_all_products(self):
        response = self.client.get("/api/products/")
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.json()), 1)

    def test_get_product_by_id(self):
        product = Product.objects.first()
        product_id = str(product.id)
        response = self.client.get(f"/api/products/{product_id}/")
        self.assertEqual(response.status_code, 200)

    def test_get_non_existent_product(self):
        response = self.client.get("/api/products/000000000000000000000000/")
        self.assertEqual(response.status_code, 404)

    # POST
    def test_create_product(self):
        category = ProductCategory.objects.first()
        data = {
            "name": "Test Product",
            "description": "A sample",
            "category": str(category.id),
            "price": "100.00",
            "brand": "TestBrand",
            "quantity": 5
        }
        response = self.client.post("/api/products/", json.dumps(data), content_type="application/json")

        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json())

    def test_create_product_missing_name(self):
        category = ProductCategory.objects.first()
        data = {
            "name": "",
            "description": "Missing name",
            "category": str(category.id),
            "price": "100.00",
            "brand": "TestBrand",
            "quantity": 5
        }
        response = self.client.post("/api/products/", json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("name", response.json())
        self.assertIn("This field may not be blank.", response.json()["name"])
        # print("RESPONSE STATUS:", response.status_code)
        # print("RESPONSE JSON:", response.json())

    def test_create_product_missing_brand(self):
        category = ProductCategory.objects.first()
        data = {
            "name": "No Brand Product",
            "description": "Missing brand",
            "category": str(category.id),
            "price": "120.00",
            "brand": "", 
            "quantity": 2
        }
        response = self.client.post("/api/products/", json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("brand", response.json())
        self.assertIn("This field may not be blank.", response.json()["brand"])

    # PUT
    def test_update_product(self):
        product = Product.objects.first()
        product_id = str(product.id)
        category_id = str(product.category.id)
        data = {
            "name": "Test Product Updated",
            "description": "A sample update",
            "category": category_id,
            "price": "101.00",
            "brand": "TestBrandUpdate",
            "quantity": 7
        }
        response = self.client.put(f"/api/products/{product_id}/", json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertIn("id", response.json())
        self.assertEqual(response.json()["name"], "Test Product Updated")
        self.assertEqual(response.json()["quantity"], 7)

    def test_update_product_invalid_price(self):
        product = Product.objects.first()
        product_id = str(product.id)
        category_id = str(product.category.id)
        data = {
            "name": "Test Product Updated",
            "description": "A sample update",
            "category": category_id,
            "price": "-10",
            "brand": "TestBrandUpdate",
            "quantity": 7
        }
        response = self.client.put(f"/api/products/{product_id}/", json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 400)

    # DELETE
    def test_delete_product(self):
        product = Product.objects.first()
        product_id = str(product.id)
        response = self.client.delete(f"/api/products/{product_id}/")
        self.assertEqual(response.status_code, 204)
        self.assertIsNone(Product.objects(id=product_id).first())


class ProductCategoryAPIIntegrationTest(SimpleTestCase):
    @classmethod
    def setUpClass(cls):
        disconnect(alias='default')
        connect(
        db="product_test_db",
        host="localhost",
        port=27017
    )
        
    def setUp(self):
        self.client = Client()
        self.seeded_data = seed() 

    def tearDown(self):
        clear()

    @classmethod
    def tearDownClass(cls):
        disconnect()

    # GET
    def test_get_all_categories(self):
        response = self.client.get("/api/categories/")
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.json()), 1)

    def test_get_category_by_id(self):
        category = ProductCategory.objects.first()
        category_id = str(category.id)
        response = self.client.get(f"/api/categories/{category_id}/")
        self.assertEqual(response.status_code, 200)

    def test_get_products_of_any_category(self):
        category = ProductCategory.objects.first()
        category_id = str(category.id)
        response = self.client.get(f"/api/categories/{category_id}/products/")
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.json()), 1)

    def test_get_non_existent_category(self):
        response = self.client.get("/api/categories/000000000000000000000000/")
        self.assertEqual(response.status_code, 404)

    # POST
    def test_create_category(self):
        data = {
            "name": "Test Category",
            "description": "A sample",
        }
        response = self.client.post("/api/categories/", json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertIn("id", response.json())

    def test_create_category_missing_description(self):   
        data = {
            "name": "Test Category",
            "description": "",
        }
        response = self.client.post("/api/categories/", json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("description", response.json())
        self.assertIn("This field may not be blank.", response.json()["description"])
    
    # PUT
    def test_update_category(self):
        category = ProductCategory.objects.first()
        category_id = str(category.id)
        data = {
            "name": "Test Category Updated",
            "description": "A sample update",
        }
        response = self.client.put(f"/api/categories/{category_id}/", json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertIn("id", response.json())
        self.assertEqual(response.json()["name"], "Test Category Updated")

    def test_update_category_missing_name(self): 
        category = ProductCategory.objects.first()
        category_id = str(category.id)
        data = {
            "name": "",
            "description": "A sample update",
        }
        response = self.client.put(f"/api/categories/{category_id}/", json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("name", response.json())
        self.assertIn("This field may not be blank.", response.json()["name"])

    # DELETE
    def test_delete_category(self):
        category = ProductCategory.objects.first()
        category_id = str(category.id)
        response = self.client.delete(f"/api/categories/{category_id}/")
        self.assertEqual(response.status_code, 204)
        self.assertIsNone(ProductCategory.objects(id=category_id).first())