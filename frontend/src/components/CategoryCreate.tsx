import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "Edit.css";

function CategoryCreate() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    name: "",
    description: "",
  });
  const [error, setError] = useState<string | null>(null);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>,
  ) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    // Form validation
    if (!formData.name || !formData.description) {
      setError("Both fields are required.");
      return;
    }

    fetch("http://127.0.0.1:8000/api/categories/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData),
    })
      .then((res) => {
        if (!res.ok) {
          throw new Error("Failed to create category");
        }
        return res.json();
      })
      .then((data) => {
        alert("Category created successfully!");
        navigate("/category");
      })
      .catch((err) => {
        console.error(err);
        setError("An error occurred while creating the category.");
      });
  };

  return (
    <div className="edit-container">
      <h2>Create New Category</h2>
      {error && <p>{error}</p>}

      <form onSubmit={handleSubmit}>
        <div>
          <label>
            Name:
            <input
              type="text"
              name="name"
              value={formData.name}
              onChange={handleChange}
            />
          </label>
        </div>
        <div>
          <label>
            Description:
            <textarea
              name="description"
              value={formData.description}
              onChange={handleChange}
              rows={4}
            />
          </label>
        </div>
        <button type="submit">Create</button>
      </form>
    </div>
  );
}

export default CategoryCreate;
