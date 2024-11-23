from fastapi import APIRouter,HTTPException
from models.shelf import Shelf,ShelfType
from schemas.shelf import ShelfRequest, ShelfResponse, ShelfTypeRequest, ShelfUpdate, ShelfTypeResponse, ShelfTypeUpdate
from dbservice import db

shelf_router=APIRouter()

# 1. shelftype(CRUD)
@shelf_router.post('/type/add')
def register_shelf_type(shelf_type: ShelfTypeRequest):
    try:
        existing_shelf_type=db.query(ShelfType).filter(
           ShelfType.company_id==shelf_type.company_id,
           ShelfType.price==shelf_type.price,
           ShelfType.description==shelf_type.description
           ).first()
        if existing_shelf_type:
            raise HTTPException(status_code=409, detail="shelf type with similar details alreeady exixts")
        
        new_shelf_type=ShelfType(
            company_id=shelf_type.company_id,
            price=shelf_type.price,
            description=shelf_type.description,
            size=shelf_type.size
        )
        db.add(new_shelf_type)
        db.commit()
        db.refresh(new_shelf_type)

        return {"message":"shelf type added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}")
    
# fetch all shelftypes
@shelf_router.get('/fetch/types', response_model=list[ShelfTypeResponse])
def get_all_registered_shelftypes():
    try:
        shelfTypes=db.query(ShelfType).all()

        return shelfTypes
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}")
    
# fetch company shelftypes
@shelf_router.get('/fetch/types/company/{company_id}', response_model=list[ShelfTypeResponse])
def get_all_registered_shelftypes(company_id: int):
    try:
        companyShelfTypes=db.query(ShelfType).filter(ShelfType.company_id==company_id).all()

        return companyShelfTypes
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}")
    
# update company shelf type
@shelf_router.put('/update/types/company/{company_id}/{shelf_id}', response_model=list[ShelfTypeResponse])
def get_all_registered_shelftypes(company_id: int, shelf_id: int, shelf_update: ShelfTypeUpdate):
    try:
        companyShelfType = db.query(ShelfType).filter(ShelfType.company_id==company_id, ShelfType.id==shelf_id).first()
        if companyShelfType is None:
            raise HTTPException(status_code=404, detail="shelf type not found")
        
        if shelf_update.description:
            companyShelfType.description==shelf_update.description

        if shelf_update.price:
            companyShelfType.price==shelf_update.price

        if shelf_update.size:
            companyShelfType.price==shelf_update.size
        
        db.commit()
        db.refresh(companyShelfType)


        return {"message":"shelftype details udated successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}")
    
# deleting the shelftype
@shelf_router.delete('/type/delete/{shelftype_id}')
def delete_shelf_type(shelftype_id: int):
    try:
        shelf_type=db.query(ShelfType).filter(ShelfType.id==shelftype_id).all()
        if shelf_type is None:
            raise HTTPException(status_code=404, detail="shelftype not found")
        
        db.delete(shelf_type)
        db.commit()

        return {"messsage":"shelftype delete succesfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}")
    
# 2. Shelf
# register shelf
@shelf_router.post('/add')
def add_shelf(shelf: ShelfRequest):
    try:
        existing_shelf=db.query(Shelf).filter(Shelf.account_number==shelf.account_number).first()

        if existing_shelf:
            raise HTTPException(status_code=409, detail="shelf with that account number already exists")
        
        new_shelf = Shelf(
            account_number=shelf.account_number,
            is_occupied=shelf.is_occupied,
            shelf_type_id=shelf.shelf_type_id
        )
        db.add(new_shelf)
        db.commit()
        db.refresh(new_shelf)
        return {"message":"shelf added successfully!"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}")
    
# fetch company shelves
@shelf_router.get('/fetch/shelves/company/{company_id}', response_model=list[ShelfResponse])
def get_all_registered_shelves(company_id: int):
    try:
        companyShelves=db.query(Shelf).join(ShelfType).filter(ShelfType.company_id==company_id).all()
        if companyShelves is None:
            raise HTTPException(status_code=404, detail="No shelved found")

        return companyShelves
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}")
    
# update shelf details

@shelf_router.put('/update/company/{company_id}/{shelf_id}', response_model=list[ShelfTypeResponse])
def get_all_registered_shelftypes(company_id: int, shelf_id: int, shelf_update: ShelfUpdate):
    try:
        companyShelf = db.query(ShelfType).filter(ShelfType.company_id==company_id, ShelfType.id==shelf_id).first()
        if companyShelf is None:
            raise HTTPException(status_code=404, detail="shelf type not found")
        
        if shelf_update.is_occupied:
            companyShelf.description=shelf_update.is_occupied

        if shelf_update.account_number:
            companyShelf.price=shelf_update.account_number

        db.commit()
        db.refresh(companyShelf)


        return {"message":"shelftype details udated successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}")
    
# remove shelf
@shelf_router.delete('/delete/shelf_id/{shelf_id}')
def delete_shelf(shelf_id: int):
    try:
        shelf=db.query(Shelf).filter(Shelf.id==shelf_id).first()
        if shelf is None:
            raise HTTPException(status_code=404, detail="No shelved found")

        db.delete(shelf)
        db.commit()

        return {"message":" shelf deleted succesfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}")

