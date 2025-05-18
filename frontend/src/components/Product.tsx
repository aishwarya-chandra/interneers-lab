import React from "react";
import { ProductType } from "./ProductList";
import { useNavigate } from "react-router-dom";
import "Product.css";

type ProductProps = ProductType & {
  isExpanded: boolean;
  onClick: () => void;
};

const Product: React.FC<ProductProps> = ({
  id,
  name,
  description,
  category,
  brand,
  price,
  quantity,
  created_at,
  updated_at,
  isExpanded,
  onClick,
}) => {
  const navigate = useNavigate();
  return (
    <div className="product-card" onClick={onClick}>
      <p>
        <strong>Name:</strong> {name}
      </p>
      {isExpanded && (
        <>
          <p>
            <strong>Description:</strong> {description}
          </p>
          <p
            className="product-category"
            onClick={(e) => {
              e.stopPropagation();
              navigate(`/category/${category}/`);
            }}
          >
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
          <p>
            <strong>Created At:</strong> {created_at}
          </p>
          <p>
            <strong>Last Update At:</strong> {updated_at}
          </p>
          <button onClick={() => navigate(`/product/${id}/`)}>Edit</button>
        </>
      )}
    </div>
  );
};

export default Product;
