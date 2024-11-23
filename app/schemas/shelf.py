from pydantic import BaseModel
from typing import Optional


# 1. Shelf type
class ShelfTypeRequest(BaseModel):
    size:str
    description:str
    price:float
    company_id:int

class ShelfTypeResponse(ShelfTypeRequest):
    id:int

class ShelfTypeUpdate(BaseModel):
    description: Optional[str]
    price: Optional[float]
    size: Optional[str]

# 2. shelf
class ShelfRequest(BaseModel):
    account_number:str
    is_occupied:bool
    shelf_type_id:int

class ShelfResponse(ShelfRequest):
    id: int

class ShelfUpdate(BaseModel):
    is_occupied: Optional[bool]
    account_number: Optional[str]  