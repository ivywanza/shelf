from fastapi import APIRouter, HTTPException
from ..schemas import CompanyRequest,CompanyResponse,CompanyUpdate, StatusResponse, StatusRequest, CompanyBranchRequest,\
CompanyBranchResponse, CompanyBranchUpdate
from dbservice import db
from ..models import Company, Status, Branch

company_router= APIRouter()

# 1. company


# register a company

@company_router.post('/register')
def register_comapny(company: CompanyRequest):
    try:
        existing_company = db.query(Company).filter(Company.company_email==company.company_email).first()

        if existing_company:
            raise HTTPException(status_code=409, detail="email already exists")
        
        new_company= Company(
            company_name=company.company_name,
            company_email=company.company_email,
            company_password=company.company_password,
            package_id=company.package_id,
            company_location=company.company_location,
            phone_number=company.phone_number

        )
        db.add(new_company)
        db.commit()
        db.refresh(new_company)

        return {"message":"Company successfully registered, welcome!"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'{str(e)}')

# fetch all existing companies
@company_router.get('/get/all/companies', response_model=list[CompanyResponse])
def fetch_all_registered_companies():
    try:
        companies= db.query(Company).all()

        return companies
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}")
    
# fetching individual companies by their unique id
@company_router.get('/get/{company_id}', response_model=CompanyResponse)
def get_company_by_id(company_id:int):
    try:
        company_details = db.query(Company).filter(Company.id==company_id).all()

        return company_details
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}")
    
# get company by the package purchased
@company_router.get('/get/{package_id}', response_model=CompanyResponse)
def get_company_by_package(package_id:int):
    try:
        companies_per_package = db.query(Company).filter(Company.id==package_id).all()

        return companies_per_package
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}")
    
# updating company details
@company_router.put('/update-details/{company_id}')
def update_company_details(update_details: CompanyUpdate, company_id:int):
    try:
        company = db.query(Company).filter(Company.id==company_id).first()

        if company is None:
            raise HTTPException(status_code=404, detail="company not found, confirm details")
        
        if update_details.company_name:
            company.company_name = update_details.company_name

        if update_details.company_email:
            company.company_email = update_details.company_email

        if update_details.phone_number:
            company.phone_number = update_details.phone_number

        if update_details.company_password:
            
            company.company_password = update_details.company_password

        if update_details.company_location:
            company.company_location = update_details.company_location

        if update_details.package_id:
            company.package_id = update_details.package_id

        if update_details.status_id:
            company.status_id = update_details.status_id

        db.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'{str(e)}')


# 2. Status
@company_router.post('/register/status')
def add_status(status: StatusRequest):
    try:
        existing_status=db.query(Status).filter(Status.name==status.name).first()

        if existing_status:
            raise HTTPException(status_code=409, detail="status already exists")
        
        new_status=Status(
            name=status.name
        )
        db.add(new_status)
        db.commit()
        db.refresh(new_status)

        return {"message":"status added successfully!"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}")
    
# get all status
@company_router.get('/get/all/status', response_model=list[StatusResponse])
def fetch_all_existing_status():
    try:
        status= db.query(Status).all()
        return status
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}")
    
# deleting status
@company_router.delete('/delete/status/{status_id}')
def delete_status(status_id:int):
    try:
        existing_status=db.query(Status).filter(Status.id==status_id).first()

        if not existing_status:
            raise HTTPException(status_code=404, detail="status not found")
        
        db.delete(existing_status)
        db.commit()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}")
    
# 3. branch

@company_router.post('/add/branch')
def add_branch(branch_details: CompanyBranchRequest):
    try:
        existing_branch=db.query(Branch).filter(
           Branch.branch_name==branch_details.branch_name, Branch.branch_location==branch_details.branch_location
           ).first()
        if existing_branch:
            raise HTTPException(status_code=409, detail="branch with that name and location already exists")
        
        new_branch=Branch(
            branch_name=branch_details.branch_name,
            branch_location=branch_details.branch_location,
            status_id=branch_details.status_id,
            company_id=branch_details.company_id
        )
        db.add(new_branch)
        db.commit()
        db.refresh(new_branch)

        return {"message":"branch added successfully!"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}")
    
# fetching all branches
@company_router.get('/get/all/branches', response_model=list[CompanyBranchResponse])
def fetch_all_registered_branches():
    try:
        branches= db.query(Branch).all()
        return branches
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}")
    
# fetch by company

@company_router.get('/get/comapany/branches/{company_id}', response_model=list[CompanyBranchResponse])
def fetch_all_registered_branches(company_id: int):
    try:
        branches= db.query(Branch).filter(Branch.company_id==company_id).all()

        if branches is None:
            raise HTTPException(status_code=404, detail="no existing branches for the given company")
        
        return branches
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}")
    
# fetch branches by company and location
@company_router.get('/get/comapany/branches/{company_id}/{branch_location}', response_model=list[CompanyBranchResponse])
def fetch_all_registered_branches(company_id: int, branch_location:int):
    try:
        branches= db.query(Branch).filter(Branch.company_id==company_id, Branch.branch_location==branch_location).all()

        if branches is None:
            raise HTTPException(status_code=404, detail="no existing branches for the given company")
        
        return branches
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}")
   
#updating branch status
@company_router.put('/update/branch_status/{branch_id}')
def update_branch_status(branch_id: int, branch_update: CompanyBranchUpdate):
    try:
        branch= db.query(Branch).filter(Branch.id==branch_id).first()

        if branch is None:
            raise HTTPException(status_code=409, detail="branch not found!")
        
        if branch_update:
            branch.status_id==branch_update

        db.commit()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}")
    
# delete branch by id
@company_router.delete('/delete/branch/{branch_id}')
def delete_branch(branch_id:int):
    try:
        existing_branch=db.query(Branch).filter(Branch.id==branch_id).first()

        if not existing_branch:
            raise HTTPException(status_code=404, detail="branch not found")
        
        db.delete(existing_branch)
        db.commit()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}")
    