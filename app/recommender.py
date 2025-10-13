# app/recommender.py
from typing import List, Dict
from db import engine
from app.models import Product
from app.llm_explain import generate_explanation

from sqlmodel import Session, select
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def recommend_products(product_id: int, top_k: int = 3) -> List[Dict]:
    """
    Generate product recommendations based on TF-IDF similarity of descriptions.
    Returns top_k similar products (excluding the input product) along with LLM explanations.

    Args:
        product_id (int): ID of the product to base recommendations on.
        top_k (int): Number of similar products to return (default=3).

    Returns:
        List[Dict]: Recommended products with id, title, similarity score, and explanation.
    """
    with Session(engine) as session:
        products = session.exec(select(Product)).all()

    # Find the index of the target product
    idx = next((i for i, p in enumerate(products) if p.id == product_id), None)
    if idx is None:
        raise ValueError(f"Product ID {product_id} not found")

    # Compute TF-IDF vectors for product descriptions
    descriptions = [p.description for p in products]
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(descriptions)

    # Compute cosine similarity and get top_k most similar products (excluding self)
    similarities = cosine_similarity(X[idx:idx+1], X).flatten()
    top_indices = np.argsort(-similarities)
    top_indices = [i for i in top_indices if i != idx][:top_k]

    # Build recommendations list with explanations
    recommendations = []
    for i in top_indices:
        product = products[i]
        recommendations.append({
            "id": product.id,
            "title": product.title,
            "score": round(float(similarities[i]), 4),
            "explanation": generate_explanation(products[idx], product)
        })

    return recommendations
