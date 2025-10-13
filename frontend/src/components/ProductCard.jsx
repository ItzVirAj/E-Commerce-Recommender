import React from "react";
import { Link } from "react-router-dom";
import "./ProductCard.css";

const ProductCard = ({ product }) => {
  const { id, title, description, image, category, price } = product;

  return (
    <Link to={`/products/${id}`} className="product-card">
      <div className="product-image">
        {image ? (
          <img src={image} alt={title} />
        ) : (
          <div className="placeholder">📦</div>
        )}
      </div>
      <div className="product-info">
        <h3>{title}</h3>
        <p className="category">{category}</p>
        <p className="description">{description}</p>
        <p className="price">${price.toFixed(2)}</p>
      </div>
    </Link>
  );
};

export default ProductCard;
