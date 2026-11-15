from fastapi import FastAPI , Depends, HTTPException
from sqlalchemy.orm import Session
import models
from database import engine, get_db
from schemas import ProductCreate , ProductResponse,LoginRequest
from auth import authenticate_user,create_token, get_current_user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/login")
def login(user_data: LoginRequest):
    if not authenticate_user(
        user_data.username,
        user_data.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )
    token = create_token(user_data.username)
    return {
        "access_token": token,
        "token_type": "bearer"
    }

@app.get('/')
def home():
    return {
        'message':'welcome to product management system',
        'status': 'API is running successfully'
    }

@app.post("/products", response_model= ProductResponse)
def create_product(
        product: ProductCreate,
        db : Session = Depends(get_db),
        current_user: str = Depends(get_current_user)
):
        
        new_product = models.Product(
              name= product.name,
              description = product.description,
              price = product.price,
              quantity = product.quantity,
              category = product.category
        )
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        return new_product

@app.get('/products/{product_id}', response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.get('/products', response_model=list[ProductResponse])
def get_products(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
            products = db.query(models.Product).all()
            return products


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