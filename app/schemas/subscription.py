from pydantic import BaseModel
from datetime import datetime

class SubscriptionPackageRequest(BaseModel):
    package_name:str
    content:str
    end_date:datetime
    price:float

class SubscriptionPackageResponse(SubscriptionPackageRequest):
    id:int

class SubscriptionPackageUpdate(SubscriptionPackageRequest):
    pass