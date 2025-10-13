import React, { useState } from "react";
import { Link } from "react-router-dom";
import "./RecommendationList.css";

const RecommendationList = ({ recommendations }) => {
  const [showExplanation, setShowExplanation] = useState({});

  if (!recommendations || recommendations.length === 0) {
    return <p>Loading Recommendations...</p>;
  }

  const toggleExplanation = (id) => {
    setShowExplanation((prev) => ({
      ...prev,
      [id]: !prev[id],
    }));
  };

  return (
    <div className="recommendation-list">
      {recommendations.map((rec) => (
        <div key={rec.id} className="rec-card-wrapper">
          <Link to={`/products/${rec.id}`} className="rec-card-link">
            <div className="rec-card">
              <div className="rec-image">
                {rec.image ? (
                  <img src={rec.image} alt={rec.title} />
                ) : (
                  <div className="placeholder">📦</div>
                )}
              </div>
              <div className="rec-info">
                <h4>{rec.title}</h4>
                <p className="category">{rec.category || "Price -- "}</p>
                <p className="price">
                  {rec.price !== undefined ? rec.price.toFixed(2) : "Check Now..!"}
                </p>
                <p className="score">
                  <strong>Score:</strong> {rec.score !== undefined ? rec.score.toFixed(3) : "N/A"}
                </p>
              </div>
            </div>
          </Link>
          {rec.explanation && (
            <button
              className="explain-btn"
              onClick={() => toggleExplanation(rec.id)}
            >
              {showExplanation[rec.id] ? "Hide Explanation" : "Why This Product?"}
            </button>
          )}
          {showExplanation[rec.id] && (
            <p className="explanation">{rec.explanation}</p>
          )}
        </div>
      ))}
    </div>
  );
};

export default RecommendationList;
