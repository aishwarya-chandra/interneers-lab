import { useState } from "react";
import { useLoaderData } from "react-router-dom";
import Product from "./Product";
import "ProductList.css";

export type ProductType = {
  id: string;
  name: string;
  description: string;
  category: string;
  brand: string;
  price: string;
  quantity: string;
};

type ProductListProps = {
  products?: ProductType[];
};

function ProductList({ products }: ProductListProps) {
  const loaderData = useLoaderData() as ProductType[];
  const data = products ?? loaderData;
  console.log(data);
  const [expandedIndex, setExpandedIndex] = useState<string | null>(null);

  const toggleExpand = (id: string) => {
    setExpandedIndex((prev) => (prev === id ? null : id));
  };

  return (
    <div>
      <h1>Product List</h1>
      {data.map((product) => (
        <Product
          key={product.id}
          {...product}
          isExpanded={expandedIndex === product.id}
          onClick={() => toggleExpand(product.id)}
        />
      ))}
    </div>
  );
}

export default ProductList;
