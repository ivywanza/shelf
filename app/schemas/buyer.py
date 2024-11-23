from pydantic import BaseModel,EmailStr
from typing import Optional
from datetime import datetime

class BuyerRequest(BaseModel):
    user_name:str
    buyer_email:str
    phone_number:str
    registration_date:datetime

class BuyerResponse(BuyerRequest):
    id:int

class BuyerUpdate(BaseModel):
    buyer_email:str
    phone_number:str