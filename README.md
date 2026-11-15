
# FastAPI – Product Management System

A beginner-friendly step-by-step guide to building a Product Management API using **FastAPI, SQLAlchemy, SQLite, and Python**.

---

## Step 1: Install Dependencies

Install Python and Visual Studio Code. Add the Python extension to VS Code.

Run the following command in the terminal:

```bash
python -m pip install fastapi uvicorn sqlalchemy
```

### Libraries Overview

| Library | Description |
|---|---|
| FastAPI | Framework to build APIs |
| Uvicorn | Web server used to run FastAPI applications |
| SQLAlchemy | Provides library support for Object-Relational Mapping (ORM) |

---

## Step 2: Create `main.py`

Create a file named `main.py` and add the following code:

```python
from fastapi import FastAPI
app = FastAPI()

@app.get("/")
async def home():
     return {
        'message':'welcome to product management system',
        'status': 'API is running successfully'
    }
```

---

## Step 3: Run the Application

Use the following command to run the application:

```bash
python -m uvicorn main:app --reload
```

Once the application starts successfully, navigate to:

**http://127.0.0.1:8000/**

> **Note:** `127.0.0.1` represents your local machine, and `8000` is the default port used by Uvicorn. Both can be changed based on your configuration.

Expected response:

```json
{
    "message": "welcome to product management system",
    "status": "API is running successfully"
}
```

---

## Step 4: Explore Swagger Documentation

FastAPI automatically generates interactive API documentation using Swagger UI.

By default, you can access it using:

**http://127.0.0.1:8000/docs**

> **Note:** `/docs` is the default Swagger UI endpoint provided by FastAPI. The host and port depend on your Uvicorn configuration. You can also customize the Swagger URL using the `docs_url` parameter in `FastAPI()`.

This allows you to explore and test API endpoints directly from the browser.

---

## Step 5: Create `database.py`

Create a file named `database.py` to configure the database connection and session management.

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = 'sqlite:///./product.db'
engine = create_engine(DATABASE_URL, connect_args={'check_same_thread':False})
SessionLocal = sessionmaker(autocommit= False,
                            autoflush=False,
                            bind=engine)
Base =declarative_base()
def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

---

## Step 6: Create `models.py`

Create a file named `models.py` to define the Product database model.

```python
from sqlalchemy import Column, Integer, String, Float
from database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    category = Column(String, nullable=False)
```

---

## Step 7: Create `schemas.py`

Create a file named `schemas.py` to define the Pydantic schemas.

```python
from pydantic import BaseModel,Field,ConfigDict

#create product
class ProductCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100, description="Name of the product")
    description: str
    price: float = Field(gt=0, description="Price of the product")
    quantity: int = Field (ge=0, description="Quantity of the product")
    category: StopAsyncIteration

#get product
class ProductResponse(ProductCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)
```

---

## Step 8: Update Imports in `main.py`

Update the imports in `main.py` to include the database, SQLAlchemy session, models, and schemas.

```python
from fastapi import FastAPI , Depends, HTTPException
from sqlalchemy.orm import Session
import models
from database import engine, get_db
from schemas import ProductCreate , ProductResponse
```

---

## Step 9: Create Database Tables

Add the following line in `main.py` to create database tables based on the defined SQLAlchemy models.

```python
models.Base.metadata.create_all(bind=engine)
```

---

## Step 10: Implement Update Product API

Add the following endpoint in `main.py` to update an existing product.

```python
@app.put('/products/{product_id}',response_model=ProductResponse)
def update_product(
            product_id : int,
            product_data: ProductCreate,
            db : Session =Depends(get_db),
            current_user: str = Depends(get_current_user)
            
):
            
            product = db.query(models.Product).filter(
                    models.Product.id == product_id
            ).first()

            if product is None:
                raise HTTPException(status_code=404, detail='product not found')
            product.name = product_data.name
            product.description = product_data.description
            product.price = product_data.price
            product.quantity = product_data.quantity
            product.category = product_data.category
            db.commit()
            db.refresh(product)
            return product
```

---

## Step 11: Implement Delete Product API

Add the following endpoint in `main.py` to delete an existing product.

```python
@app.delete("/products/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
     current_user: str = Depends(get_current_user)
):
    product = db.query(models.Product).filter(
        models.Product.id == product_id
    ).first()
    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )
    db.delete(product)
    db.commit()
    return {
        "message": "Product deleted successfully"
    }
```

---

## Step 12: Test the APIs Using Swagger

Navigate to the default Swagger UI URL:

**http://127.0.0.1:8000/docs**

Try updating and deleting a product using the Swagger interface to verify that the APIs are working as expected.

---

## Technologies Used

- Python
- FastAPI
- Uvicorn
- SQLAlchemy
- SQLite
- Pydantic
- Swagger UI

---

**Happy Coding! 🚀**
