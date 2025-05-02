import React from "react";
import logo from "./logo.svg";
import "./App.css";
import ProductList from "components/ProductList";
import Header from "components/Header";

function App() {
  return (
    <div className="App">
      <div>
        <Header />
        <ProductList />
      </div>
    </div>
  );
}

export default App;
