from pydantic import BaseModel,Field,ConfigDict

class LoginRequest(BaseModel):
    username : str
    password :str
    
class TokenResponse(BaseModel):
    access_token : str
    token_type : str

#create product
class ProductCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100, description="Name of the product")
    description: str
    price: float = Field(gt=0, description="Price of the product")
    quantity: int = Field (ge=0, description="Quantity of the product")
    category: str

    
class ProductResponse(ProductCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)