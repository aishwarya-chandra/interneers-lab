import { useEffect, useState } from "react";
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
  const [data, setData] = useState<ProductType[]>(products ?? []);
  const [next, setNext] = useState<string | null>(null);
  const [previous, setPrevious] = useState<string | null>(null);
  const [currentUrl, setCurrentUrl] = useState(
    "http://127.0.0.1:8000/api/products/?page=1&page_size=5",
  );
  const [expandedIndex, setExpandedIndex] = useState<string | null>(null);

  const toggleExpand = (id: string) => {
    setExpandedIndex((prev) => (prev === id ? null : id));
  };

  useEffect(() => {
    if (products) return;

    fetch(currentUrl)
      .then((res) => res.json())
      .then((res) => {
        setData(res.results);
        setNext(res.next);
        setPrevious(res.previous);
      });
  }, [products, currentUrl]);

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

      {/* Pagination controls*/}
      {!products && (
        <div style={{ marginTop: "1rem", display: "flex", gap: "1rem" }}>
          <button
            onClick={() => previous && setCurrentUrl(previous)}
            disabled={!previous}
          >
            Previous
          </button>
          <button onClick={() => next && setCurrentUrl(next)} disabled={!next}>
            Next
          </button>
        </div>
      )}
    </div>
  );
}

export default ProductList;
