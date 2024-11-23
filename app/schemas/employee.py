from pydantic import BaseModel, EmailStr
from typing import Optional

# role
class RoleRequest(BaseModel):
    roleName:str
    company_id: Optional[int]

class RoleResponse(RoleRequest):
    id:int

class EmployeeRequest(BaseModel):
    employee_name: str
    company_id: int
    national_id_number: str
    password: str
    branch_id: int
    role_id: int
    employee_email: EmailStr

class EmployeeResponse(EmployeeRequest):
    id: int
    is_active: bool

class EmployeeUpdate(BaseModel):
    is_active: Optional[bool]
    role_id: Optional[int]
    employee_email: Optional[str]