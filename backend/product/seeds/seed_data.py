from decimal import Decimal
from product.models import ProductCategory, Product

def seed():
    
    # Clear existing data
    Product.drop_collection()
    ProductCategory.drop_collection()

    # Seed product categories
    electronics = ProductCategory(name="Electronics", description="Devices and gadgets")
    fashion = ProductCategory(name="Fashion", description="Clothing and accessories")
    electronics.save()
    fashion.save()

    # Seed products
    laptop = Product(
        name="Laptop",
        description="High-performance laptop",
        category=electronics,
        price=Decimal("1200.00"),
        brand="Dell",
        quantity=10
    )
    tshirt = Product(
        name="T-Shirt",
        description="100% cotton t-shirt",
        category=fashion,
        price=Decimal("20.00"),
        brand="H&M",
        quantity=50
    )

    laptop.save()
    tshirt.save()

if __name__ == "__main__":
    seed()
