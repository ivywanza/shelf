from fastapi import APIRouter, HTTPException
from ..schemas import SubscriptionPackageRequest, SubscriptionPackageResponse, SubscriptionPackageUpdate
from ..dbservice import db
from ..models import Package


subscription_router=APIRouter()

# adding packages

@subscription_router.post('/add_package')
def add_subscription_package(package: SubscriptionPackageRequest):
    try:
        new_package=Package(
            package_name= package.package_name,
            end_date= package.end_date,
            content= package.content,
            price= package.price

        )
        db.add(new_package)
        db.commit()
        db.refresh(new_package)

        return {"message":"subscription package added successfully!"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}")
    
# fetching all available subscription packages
@subscription_router.get('/fetch/all', response_model=list[SubscriptionPackageResponse])
def fetch_all_packages():
    try:
        packages= db.query(Package).all()

        return packages
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}")
    

# fetching by id
@subscription_router.get('/fetch/id/{package_id}', response_model=list[SubscriptionPackageResponse])
def fetch_all_packages(package_id:int):
    try:
        packages= db.query(Package).filter(Package.id==package_id).all()
        return packages
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}")
    
    
# update package details
@subscription_router.put('/update/package_id/{package_id}')
def update_package_details(package_id:int, new_details:SubscriptionPackageUpdate):
    try:
        package=db.query(Package).filter(Package.id==package_id).first()

        if new_details.package_name:
           package.package_name==new_details.package_name

        if new_details.content:
           package.content==new_details.content

        if new_details.end_date:
           package.end_date==new_details.end_date

        if new_details.price:
           package.price==new_details.price


        if package is None:
           raise HTTPException(status_code=404, detail="package doesn't exist!")
       
        db.commit()

        return {"message":"package updated successfully!"}

       
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}")
    
# delete a subscription package
@subscription_router.delete('/delete/{package_id}')
def delete_package(package_id: int):
    try:
        packages= db.query(Package).filter(Package.id==package_id).first()
        db.delete(packages)
        db.commit()
        db.refresh(packages)
        return {"message":"Deleted!"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}")