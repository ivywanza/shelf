from pydantic import BaseModel,EmailStr
from typing import Optional
from datetime import datetime


class CompanyRequest(BaseModel):
    company_name:str
    company_email:EmailStr
    phone_number:str
    company_password:str
    company_location:str
    # role_id:int
    package_id:int

class CompanyResponse(CompanyRequest):
    id:int
    registration_date : datetime
    is_active: bool


class CompanyUpdate(BaseModel):
    company_name: Optional[str]
    company_email: Optional[str]
    phone_number: Optional[str]
    company_password: Optional[str]
    company_location: Optional[str]
    package_id: Optional[int]
    is_active: Optional[bool]


# status

class StatusRequest(BaseModel):
    name:str
    company_id: int

class StatusResponse(StatusRequest):
    id:int

# company branch

class CompanyBranchRequest(BaseModel):
    branch_location:str
    branch_name:str
    company_id: int

class CompanyBranchResponse(CompanyBranchRequest):
    id:int

class CompanyBranchUpdate(BaseModel):
    is_active: Optional[bool]
