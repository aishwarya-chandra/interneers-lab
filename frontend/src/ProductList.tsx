import { useState } from "react";
import Product from "Product";

const dummyProducts = [
  {
    name: "MacBook Pro",
    description: "A smart computer",
    category: "Electronics",
    brand: "Apple",
    price: "$1999",
    quantity: "10",
  },
  {
    name: "Galaxy S23",
    description: "Flagship Android smartphone",
    category: "Mobiles",
    brand: "Samsung",
    price: "$899",
    quantity: "25",
  },
  {
    name: "Sony WH-1000XM5",
    description: "Noise-cancelling headphones",
    category: "Audio",
    brand: "Sony",
    price: "$349",
    quantity: "15",
  },
  {
    name: "Dell XPS 13",
    description: "Compact and powerful laptop",
    category: "Computers",
    brand: "Dell",
    price: "$1399",
    quantity: "8",
  },
  {
    name: "Apple Watch Series 9",
    description: "Smartwatch with health tracking",
    category: "Wearables",
    brand: "Apple",
    price: "$499",
    quantity: "12",
  },
  {
    name: "Canon EOS R10",
    description: "Mirrorless camera with 24MP sensor",
    category: "Cameras",
    brand: "Canon",
    price: "$999",
    quantity: "5",
  },
  {
    name: "Google Nest Thermostat",
    description: "Smart thermostat for home automation",
    category: "Home Tech",
    brand: "Google",
    price: "$129",
    quantity: "30",
  },
];

function ProductList() {
  const [expandedIndex, setExpandedIndex] = useState<number | null>(null);

  const toggleExpand = (index: number) => {
    setExpandedIndex((prev) => (prev === index ? null : index));
  };

  return (
    <div>
      <h1>Products List</h1>
      {dummyProducts.map((product, index) => (
        <Product
          key={index}
          {...product}
          isExpanded={expandedIndex === index}
          onClick={() => toggleExpand(index)}
        />
      ))}
    </div>
  );
}

export default ProductList;
