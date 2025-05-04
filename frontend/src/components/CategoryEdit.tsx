import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import "Edit.css";

function CategoryEdit() {
  const { catId } = useParams();
  const [formData, setFormData] = useState({
    name: "",
    description: "",
  });

  useEffect(() => {
    fetch(`http://127.0.0.1:8000/api/categories/${catId}/`)
      .then((res) => res.json())
      .then((data) => {
        setFormData({
          name: data.name || "",
          description: data.description || "",
        });
      });
  }, [catId]);

  console.log(formData);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>,
  ) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const navigate = useNavigate();
  const handleUpdate = () => {
    fetch(`http://127.0.0.1:8000/api/categories/${catId}/`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData),
    })
      .then(async (res) => {
        if (!res.ok) {
          const errorData = await res.json();
          console.log(errorData);
          const errorMessages = Object.entries(errorData)
            .map(([field, messages]) => `${field}: ${messages as string[]}`)
            .join("\n");
          alert("Error updating category:\n" + errorMessages);
          throw new Error("Validation failed");
        }
        return res.json();
      })
      .then((data) => {
        alert("Category updated successfully!");
        navigate(`/category/${catId}`);
      })
      .catch((err) => {
        console.error("Error saving category:", err);
      });
  };

  return (
    <>
      <div className="edit-container">
        <div>
          <h2>Edit Category</h2>
        </div>
        <div>
          <label>Name: </label>
          <input
            name="name"
            value={formData.name}
            onChange={handleChange}
            placeholder="Name"
          />
        </div>
        <div>
          <label>Description: </label>
          <input
            name="description"
            value={formData.description}
            onChange={handleChange}
            placeholder="Description"
          />
        </div>
        <div>
          <button onClick={handleUpdate}>Update</button>
        </div>
      </div>
    </>
  );
}

export default CategoryEdit;
