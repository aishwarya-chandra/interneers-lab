function Navbar() {
  return (
    <nav
      style={{
        backgroundColor: "#f4f4f4",
        padding: "0.5rem 1rem",
        display: "flex",
        gap: "1rem",
        borderBottom: "1px solid #ccc",
      }}
    >
      <a href="#" style={{ textDecoration: "none", color: "#333" }}>
        Home
      </a>
      <a href="#" style={{ textDecoration: "none", color: "#333" }}>
        Products
      </a>
    </nav>
  );
}

export default Navbar;
