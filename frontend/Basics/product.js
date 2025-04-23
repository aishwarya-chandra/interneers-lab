// API fetch in console
// fetch("http://127.0.0.1:8000/api/products/")
//   .then(response => response.json())
//   .then(data => {
//     console.log("API Data:", data);
//   })
//   .catch(error => {
//     console.error("Error fetching data:", error);
//   });


//API fetch in the web page
const API_URL = "http://127.0.0.1:8000/api/products/";

fetch(API_URL)
  .then((response) => response.json())
  .then((data) => {
    const container = document.getElementById("product-container");

    data.forEach((product) => {
      const tile = document.createElement("div");
      tile.className = "product-tile";
      tile.innerHTML = `
        <p><strong>Name:</strong> ${product.name}</p>
        <p><strong>Description:</strong> ${product.description}</p>
        <p><strong>Category:</strong> ${product.category}</p>
        <p><strong>Brand:</strong> ${product.brand}</p>
        <p><strong>Price:</strong> ₹${product.price}</p>
        <p><strong>Quantity:</strong> ${product.quantity}</p>
      `;
      container.appendChild(tile);
    });
  })
  .catch((err) => console.error("Error fetching data:", err));
