import React from "react";
import ReactDOM from "react-dom/client";
import reportWebVitals from "./reportWebVitals";
import {
  createBrowserRouter,
  createRoutesFromElements,
  Route,
  RouterProvider,
} from "react-router-dom";
import ProductList from "components/ProductList";
import Layout from "components/Layout";
import Home from "components/Home";
import { CategoriesInfoLoader } from "components/DataLoader";
import ProductEdit from "components/ProductEdit";
import CategoryList from "components/CategoryList";
import CategoryInfo from "components/CategoryInfo";
import CategoryEdit from "components/CategoryEdit";
import CategoryCreate from "components/CategoryCreate";

const router = createBrowserRouter(
  createRoutesFromElements(
    <Route path="/" element={<Layout />}>
      <Route path="" element={<Home />} />
      <Route path="product" element={<ProductList />} />
      <Route
        loader={CategoriesInfoLoader}
        path="product/:id"
        element={<ProductEdit />}
      />
      <Route
        loader={CategoriesInfoLoader}
        path="category"
        element={<CategoryList />}
      />
      <Route path="category/:catId" element={<CategoryInfo />} />
      <Route path="category/:catId/edit" element={<CategoryEdit />} />
      <Route path="category/new" element={<CategoryCreate />} />
    </Route>,
  ),
);

const root = ReactDOM.createRoot(
  document.getElementById("root") as HTMLElement,
);
root.render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>,
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
