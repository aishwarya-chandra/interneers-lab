export const CategoriesInfoLoader = async () => {
  const response = await fetch("http://127.0.0.1:8000/api/categories/");
  return response.json();
};
