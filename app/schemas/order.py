from pydantic import BaseModel,EmailStr
from typing import Optional
from datetime import datetime


class OrderRequest(BaseModel):
    order_number:str
    buyer_id:int
    product_id:int
    quantity:int
    totalPrice:float
    status_id:int

class OrderResponse(OrderRequest):
    id:int

class OrderUpdate(BaseModel):
    product_id:int
    quantity:int
    totalPrice:float
    status_id:int