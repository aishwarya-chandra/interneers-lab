import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import ProductList from "./ProductList";
import { ProductType } from "./ProductList";
import "CategoryInfo.css";

function CategoryInfo() {
  const { catId } = useParams();
  const [category, setCategory] = useState<{
    id: string;
    name: string;
    description: string;
  } | null>(null);
  const [categoryProduct, setCategoryProduct] = useState<ProductType[] | null>(
    null,
  );

  // Fetch category details
  useEffect(() => {
    fetch(`http://127.0.0.1:8000/api/categories/${catId}/`)
      .then((res) => res.json())
      .then((res) => setCategory(res));
  }, [catId]);

  // Fetch products for the category
  useEffect(() => {
    fetch(`http://127.0.0.1:8000/api/categories/${catId}/products/`)
      .then((res) => res.json())
      .then((res) => setCategoryProduct(res));
  }, [catId]);

  const navigate = useNavigate();

  // Handle category deletion
  const handleDelete = () => {
    const confirmDelete = window.confirm(
      "Are you sure you want to delete this category?",
    );
    if (!confirmDelete) return;

    fetch(`http://127.0.0.1:8000/api/categories/${catId}/`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((res) => {
        if (res.ok) {
          alert("Category deleted successfully!");
          navigate("/category/");
        } else {
          return res.json().then((data) => {
            throw new Error(data.message || "Failed to delete category.");
          });
        }
      })
      .catch((err) => {
        console.error("Error deleting category:", err);
        alert("Error deleting category: " + err.message);
      });
  };

  return (
    <div className="category-info-container">
      <h1>Category Information</h1>
      {category ? (
        <div>
          <p>
            <strong>Name:</strong> {category.name}
          </p>
          <p>
            <strong>Description:</strong> {category.description}
          </p>
        </div>
      ) : (
        <p className="loading">Loading category...</p>
      )}

      {categoryProduct ? (
        categoryProduct.length > 0 ? (
          <div>
            <ProductList products={categoryProduct} />
          </div>
        ) : (
          <div>
            <h1>Product List</h1>
            <p>No products found for this category</p>
          </div>
        )
      ) : (
        <p className="loading">Loading products...</p>
      )}

      <div>
        <button onClick={handleDelete} className="delete-category-button">
          Delete Category
        </button>
        <button
          onClick={() => navigate(`/category/${catId}/edit`)}
          className="category-info-button"
        >
          Edit Category
        </button>
      </div>
    </div>
  );
}

export default CategoryInfo;
