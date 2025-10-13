# app/main.py
from fastapi import FastAPI, HTTPException
from sqlmodel import select
from db import get_session, init_db
from app.models import Product
from app.recommender import recommend_products
from typing import List
from fastapi.middleware.cors import CORSMiddleware


# Initialize database from CSV if empty
init_db(csv_path="sample_data.csv")


app = FastAPI(title="E-Commerce Recommender API")

# ✅ Add CORS so React frontend can talk to FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------- ROOT -----------------
@app.get("/")
def root():
    return {"message": "Welcome to the E-Commerce Recommender API"}


# ----------------- PRODUCTS CRUD -----------------

@app.get("/products/", response_model=List[Product])
def list_products():
    """List all products in the catalog"""
    with get_session() as session:
        products = session.exec(select(Product)).all()
    return products


@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int):
    """Get product details by ID"""
    with get_session() as session:
        product = session.get(Product, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.post("/products/", response_model=Product)
def create_product(product: Product):
    """Add a new product to the catalog"""
    with get_session() as session:
        session.add(product)
        session.commit()
        session.refresh(product)
    return product


@app.put("/products/{product_id}", response_model=Product)
def update_product(product_id: int, updated_product: Product):
    """Update an existing product"""
    with get_session() as session:
        product = session.get(Product, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        product.title = updated_product.title
        product.description = updated_product.description
        product.category = updated_product.category
        product.price = updated_product.price
        session.add(product)
        session.commit()
        session.refresh(product)
    return product


@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    """Delete a product by ID"""
    with get_session() as session:
        product = session.get(Product, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        session.delete(product)
        session.commit()
    return {"message": f"Product {product_id} deleted successfully"}


# ----------------- RECOMMENDATIONS -----------------

@app.get("/products/{product_id}/recommendations")
def get_recommendations(product_id: int):
    """
    Get top 3 product recommendations for a given product.
    Each recommendation includes:
      - Product ID
      - Title
      - Similarity score
      - LLM-generated explanation
    """
    try:
        recommendations = recommend_products(product_id)
        return {
            "product_id": product_id,
            "recommendations": recommendations
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
