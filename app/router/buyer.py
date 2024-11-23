from fastapi import APIRouter,HTTPException
from schemas.buyer import BuyerRequest,BuyerResponse,BuyerUpdate
from models.buyer import Buyer
from dbservice import db
from datetime import datetime

buyer_router=APIRouter()

# Create a new buyer
@buyer_router.post("/", response_model=BuyerResponse)
def create_buyer(buyer_request: BuyerRequest):
    try:
        new_buyer = Buyer(**buyer_request.dict())
        db.add(new_buyer)
        db.commit()
        db.refresh(new_buyer)
        return new_buyer
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# Get all buyers
@buyer_router.get("/", response_model=list[BuyerResponse])
def get_buyers():
    try:
        buyers = db.query(Buyer).all()
        return buyers
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Get a single buyer by ID

@buyer_router.get("/{buyer_id}", response_model=BuyerResponse)
def get_buyer(buyer_id: int):
    try:
        buyer = db.query(Buyer).filter(Buyer.id == buyer_id).first()
        if not buyer:
            raise HTTPException(status_code=404, detail="Buyer not found")
        return buyer
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Update a buyer
@buyer_router.put("/{buyer_id}", response_model=BuyerResponse)
def update_buyer(buyer_id: int, buyer_update: BuyerUpdate):
    try:
        buyer = db.query(Buyer).filter(Buyer.id == buyer_id).first()
        if not buyer:
            raise HTTPException(status_code=404, detail="Buyer not found")

        if buyer_update.buyer_email:
            buyer.buyer_email=buyer_update.buyer_email

        if buyer_update.phone_number:
            buyer.phone_number=buyer_update.phone_number

        
        db.commit()
        db.refresh(buyer)
        return buyer
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# Delete a buyer
@buyer_router.delete("/{buyer_id}")
def delete_buyer(buyer_id: int):
    try:
        buyer = db.query(Buyer).filter(Buyer.id == buyer_id).first()
        if not buyer:
            raise HTTPException(status_code=404, detail="Buyer not found")

        db.delete(buyer)
        db.commit()
        return {"message": "Buyer deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))