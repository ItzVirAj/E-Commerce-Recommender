import React, { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { getRecommendations, getProducts } from "../api";
import RecommendationList from "../components/RecommendationList";
import "./ProductPage.css";

const ProductPage = () => {
  const { id } = useParams();
  const [product, setProduct] = useState(null);
  const [recommendations, setRecommendations] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const allProducts = await getProducts();
        const selectedProduct = allProducts.find((p) => p.id === parseInt(id));
        setProduct(selectedProduct);

        const recs = await getRecommendations(id);
        setRecommendations(recs.recommendations || []);
      } catch (error) {
        console.error(error);
      }
    };
    fetchData();
  }, [id]);

  if (!product) return <p>Loading product...</p>;

  return (
    <div className="product-page">
      <Link to="/" className="back-link">← Back</Link>
      <div className="product-container">
        {/* Left Column: Selected Product */}
        <div className="left-column">
          <div className="product-card-detail">
            <div className="product-image">
              {product.image ? <img src={product.image} alt={product.title} /> : <div className="placeholder">📦</div>}
            </div>
            <div className="product-info">
              <h2>{product.title}</h2>
              <p className="category">{product.category}</p>
              <p className="description">{product.description}</p>
              <p className="price">${product.price.toFixed(2)}</p>
            </div>
          </div>
        </div>

        {/* Right Column: Recommendations */}
        <div className="right-column">
          <h2>Recommended Products</h2>
          <RecommendationList recommendations={recommendations} />
        </div>
      </div>
    </div>
  );
};

export default ProductPage;
