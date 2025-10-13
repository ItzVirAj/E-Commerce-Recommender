import csv
from sqlmodel import SQLModel, Session, create_engine, select
from app.models import Product

# Database engine
engine = create_engine("sqlite:///database.db", echo=True)

def init_db(csv_path: str = "sample_data.csv"):
    """Create tables and populate products from CSV if empty."""
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        # Check if any products exist
        product_exists = session.exec(select(Product)).first()
        if not product_exists:
            try:
                with open(csv_path, newline='', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    products = [
                        Product(
                            id=int(row["id"]) if "id" in row and row["id"] else None,
                            title=row["title"],
                            description=row["description"],
                            category=row["category"],
                            price=float(row["price"]) if "price" in row and row["price"] else None
                        )
                        for row in reader
                    ]
                    session.add_all(products)
                    session.commit()
                    print(f"Inserted {len(products)} products from {csv_path}.")
            except FileNotFoundError:
                print(f"CSV file '{csv_path}' not found. No products added.")

def get_session() -> Session:
    """Return a new database session."""
    return Session(engine)

# Initialize database on direct execution
if __name__ == "__main__":
    init_db(csv_path="sample_data.csv")
