//a single reusable component to project dummy data
import React from "react";

type ProductProps = {
  name: string;
  description: string;
  category: string;
  brand: string;
  price: string;
  quantity: string;
  isExpanded: boolean;
  onClick: () => void;
};

const Product: React.FC<ProductProps> = ({
  name,
  description,
  category,
  brand,
  price,
  quantity,
  isExpanded,
  onClick,
}) => {
  return (
    <div
      className="product-card"
      onClick={onClick}
      style={{
        cursor: "pointer",
        marginBottom: "1rem",
        border: "1px solid #ccc",
        padding: "1rem",
        borderRadius: "8px",
      }}
    >
      <p>
        <strong>Name:</strong> {name}
      </p>
      {isExpanded && (
        <>
          <p>
            <strong>Description:</strong> {description}
          </p>
          <p>
            <strong>Category:</strong> {category}
          </p>
          <p>
            <strong>Brand:</strong> {brand}
          </p>
          <p>
            <strong>Price:</strong> {price}
          </p>
          <p>
            <strong>Quantity:</strong> {quantity}
          </p>
        </>
      )}
    </div>
  );
};

export default Product;
