from product.models import Product, ProductCategory

def clear():

    Product.drop_collection()
    ProductCategory.drop_collection()

if __name__ == "__main__":
    clear()
