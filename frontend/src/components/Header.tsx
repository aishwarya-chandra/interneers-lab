import React from "react";
import { NavLink } from "react-router-dom";
import "Header.css";

function Header() {
  return (
    <>
      <ul>
        <li>
          <NavLink to="/">Home</NavLink>
        </li>
        <li>
          <NavLink to="product">Products</NavLink>
        </li>
        <li>
          <NavLink to="category">Categories</NavLink>
        </li>
      </ul>
    </>
  );
}

export default Header;
