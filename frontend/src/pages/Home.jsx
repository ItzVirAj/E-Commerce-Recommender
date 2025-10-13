import React, { useEffect, useState } from "react";
import { getProducts } from "../api";
import ProductCard from "../components/ProductCard";
import "./Home.css";

const Home = () => {
  const [products, setProducts] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState("All");
  const [categories, setCategories] = useState(["All"]);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const data = await getProducts();
        setProducts(data);

        const uniqueCategories = ["All", ...new Set(data.map((p) => p.category))];
        setCategories(uniqueCategories);
      } catch (error) {
        console.error("Failed to fetch products:", error);
      }
    };

    fetchProducts();
  }, []);

  const filteredProducts =
    selectedCategory === "All"
      ? products
      : products.filter((p) => p.category === selectedCategory);

  return (
    <div className="home">
      {/* Header with GitHub and Website Buttons */}
      <header className="home-header">
        <h1>E-Commerce AI Recommendations</h1>
        <div className="header-buttons">
          <a
            href="https://github.com/ItzVirAj"
            target="_blank"
            rel="noopener noreferrer"
            className="header-btn"
          >
            GitHub
          </a>
          <a
            href="https://viruum.vercel.app/"
            target="_blank"
            rel="noopener noreferrer"
            className="header-btn"
          >
            My Website
          </a>
        </div>
      </header>

      {/* Category Menu */}
      <div className="category-menu">
        {categories.map((cat) => (
          <button
            key={cat}
            className={`category-btn ${selectedCategory === cat ? "active" : ""}`}
            onClick={() => setSelectedCategory(cat)}
          >
            {cat}
          </button>
        ))}
      </div>

      {/* Products Grid */}
      <div className="grid">
        {filteredProducts.length > 0 ? (
          filteredProducts.map((product) => (
            <ProductCard key={product.id} product={product} />
          ))
        ) : (
          <p className="no-products">No products available in this category.</p>
        )}
      </div>
    </div>
  );
};

export default Home;
