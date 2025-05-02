import React, { useEffect, useState } from "react";
import { useLoaderData, useNavigate, useParams } from "react-router-dom";
import { CategoryType } from "./CategoryList";
import "Edit.css";

function ProductEdit() {
  const navigate = useNavigate();
  const { id } = useParams();
  const [formData, setFormData] = useState({
    name: "",
    description: "",
    category: "",
    brand: "",
    price: "",
    quantity: "",
  });

  const category = useLoaderData() as CategoryType[];

  useEffect(() => {
    fetch(`http://127.0.0.1:8000/api/products/${id}/`)
      .then((res) => res.json())
      .then((data) => {
        setFormData({
          name: data.name || "",
          description: data.description || "",
          category: data.category || "",
          brand: data.brand || "",
          price: data.price || "",
          quantity: data.quantity || "",
        });
      });
  }, [id]);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>,
  ) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSave = () => {
    fetch(`http://127.0.0.1:8000/api/products/${id}/`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData),
    })
      .then(async (res) => {
        if (!res.ok) {
          const errorData = await res.json();
          const errorMessages = Object.entries(errorData)
            .map(([field, messages]) => `${field}: ${messages as string[]}`)
            .join("\n");
          alert("Error updating product:\n" + errorMessages);
          throw new Error("Validation failed");
        }
        return res.json();
      })
      .then(() => {
        alert("Product updated successfully!");
        navigate("/product/");
      })
      .catch((err) => {
        console.error("Error saving product:", err);
      });
  };

  return (
    <div className="edit-container">
      <h2>Edit Product</h2>

      <div>
        <label>Name:</label>
        <input
          name="name"
          value={formData.name}
          onChange={handleChange}
          placeholder="Name"
        />
      </div>

      <div>
        <label>Description:</label>
        <input
          name="description"
          value={formData.description}
          onChange={handleChange}
          placeholder="Description"
        />
      </div>

      <div>
        <label>Category:</label>
        <select
          name="category"
          value={formData.category}
          onChange={handleChange}
        >
          {category.map((cat) => (
            <option key={cat.id} value={cat.id}>
              {cat.name}
            </option>
          ))}
        </select>
      </div>

      <div>
        <label>Brand:</label>
        <input
          name="brand"
          value={formData.brand}
          onChange={handleChange}
          placeholder="Brand"
        />
      </div>

      <div>
        <label>Price:</label>
        <input
          name="price"
          value={formData.price}
          onChange={handleChange}
          placeholder="Price"
        />
      </div>

      <div>
        <label>Quantity:</label>
        <input
          name="quantity"
          value={formData.quantity}
          onChange={handleChange}
          placeholder="Quantity"
        />
      </div>

      <div>
        <button onClick={handleSave}>Save</button>
      </div>
    </div>
  );
}

export default ProductEdit;
