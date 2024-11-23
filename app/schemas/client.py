from pydantic import BaseModel, EmailStr
from datetime import datetime

class ClientRequest(BaseModel):
    company_id: int
    client_name: str
    client_email: EmailStr
    phone_number:str
    shelf_id: int

class ClientResponse(ClientRequest):
    id: int
    start_date: datetime

class ClientUpdate(BaseModel):
    client_email: EmailStr
    phone_number:str
    shelf_id:int

class ProductRequest(BaseModel):
    client_id:int
    productName:str
    productPrice:float
    stock_quantity:int
    shelf_id:int

class ProductResponse(ProductRequest):
    id:int

class ProductUpdate(BaseModel):
    productName:str
    productPrice:float
    stock_quantity:int
    shelf_id:int
    last_updated:datetime