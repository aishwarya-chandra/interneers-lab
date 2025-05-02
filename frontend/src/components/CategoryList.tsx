import React from "react";
import { useLoaderData, useNavigate } from "react-router-dom";
import "CategoryList.css";

export type CategoryType = {
  id: string;
  name: string;
  description: string;
};

function CategoryList() {
  const categoriesData = useLoaderData() as CategoryType[];
  const navigate = useNavigate();

  return (
    <div className="category-list-container">
      <h1>Category List</h1>

      <div style={{ marginBottom: "1rem" }}>
        <button
          onClick={() => navigate("/category/new")}
          className="create-category-button"
        >
          Create New Category
        </button>
      </div>

      <div>
        {categoriesData.map((cat) => (
          <div
            key={cat.id}
            className="category-card"
            onClick={() => navigate(`${cat.id}`)}
          >
            {cat.name}
          </div>
        ))}
      </div>
    </div>
  );
}

export default CategoryList;
