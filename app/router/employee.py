from schemas.employee import EmployeeRequest, EmployeeResponse ,EmployeeUpdate, RoleRequest, RoleResponse
from dbservice import db
from models.employee import Role, Employee
from fastapi import APIRouter, HTTPException

employee_router=APIRouter()

# 1. Role

# register
@employee_router.post('/role/register')
def add_role(role: RoleRequest):
    try:
        existing_role=db.query(Role).filter(Role.roleName==role.roleName, Role.company_id==role.company_id).first()

        if existing_role:
            raise HTTPException(status_code=409, detail="role already exists")
        
        register_role=Role(
            roleName=role.roleName,
            company_id=role.company_id
        )
        db.add(register_role)
        db.commit()
        db.refresh(register_role)

        return {"message":"new role added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}")
    
# fetch all roles
@employee_router.get('/get/all/roles', response_model=list[RoleResponse])
def fetch_all_existing_roles():
    try:
        roles= db.query(Role).all()
        return roles
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}")
    
# get company roles
@employee_router.get('/get/company/roles/{company_id}', response_model=list[RoleResponse])
def fetch_company_existing_roles(company_id: int):
    try:
        company_roles= db.query(Role).filter(Role.company_id==company_id).all()

        if company_roles is None:
            raise HTTPException(status_code=404, detail="No roles exist for this company")

        return company_roles
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}")
    
# delete company roles by role_id 
@employee_router.delete('/delete/roles/{company_id}/{role_id}')
def delete_company_roles(company_id: int, role_id: int):
    try:
        role= db.query(Role).filter(Role.id==role_id,Role.company_id==company_id).first()

        if not role:
           raise HTTPException(status_code=404, detail="role doesn't exist")
        
        db.delete(role)
        db.commit()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}")
    
# delete all roles for that company
@employee_router.delete('/delete/roles/{company_id}')
def delete_company_roles(company_id: int):
    try:
        role= db.query(Role).filter(Role.company_id==company_id).first()

        if not role:
           raise HTTPException(status_code=404, detail="company has no registered roles")
        
        db.delete(role)
        db.commit()
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}")
 
# 2. Employees(CRUD)
@employee_router.post('/employee/register')
def register_employee(employee: EmployeeRequest):
    try:
        existing_employee= db.query(Employee.national_id_number==employee.national_id_number).first()

        if existing_employee:
           raise HTTPException(status_code=409, detail="employee eith this id already exists")
       
        new_employee=Employee(
            employee_email=employee.employee_email,
            employee_name=employee.employee_name,
            national_id_number=employee.national_id_number,
            password=employee.password,
            branch_id=employee.branch_id,
            role_id=employee.role_id,
            company_id=employee.company_id

        )
        db.add(new_employee)
        db.commit()
        db.refresh(new_employee)

        return {"message":"employee registered successfully!"}       
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}")
    
# fetch all company employees
@employee_router.get('/get/company/employees/{company_id}', response_model=list[EmployeeResponse])
def fetch_company_registered_employees(company_id: int):
    try:
        company_employees= db.query(Employee).filter(Employee.company_id==company_id).all()

        if company_employees is None:
            raise HTTPException(status_code=404, detail="No registered employees for this company")

        return company_employees
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}")
    
# fetch company employees by their status
@employee_router.get('/get/company/employees/{company_id}/{is_active}', response_model=list[EmployeeResponse])
def fetch_company_registered_employees(company_id: int, is_active: bool):
    try:
        company_employees= db.query(Employee).filter(Employee.company_id==company_id, Employee.is_active==is_active).all()

        if company_employees is None:
            raise HTTPException(status_code=404, detail="No registered employees for this company")

        return company_employees
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}")
    
# update employee details
@employee_router.put('/employee/update/{employee_id}')
def update_employee_details(employee_id: int, request: EmployeeUpdate):
    try:
        employee= db.query(Employee).filter(Employee.id==employee_id).first()

        if employee is None:
            raise HTTPException(status_code=404, detail="Employee does not exist")
        
        if request.is_active:
            employee.is_active=request.is_active

        if request.role_id:
            employee.role_id=request.role_id

        if request.employee_email:
            employee.employee_email=request.employee_email

        db.commit()
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}")
    


