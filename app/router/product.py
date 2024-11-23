from fastapi import APIRouter,HTTPException
from schemas.client import ProductRequest,ProductResponse,ProductUpdate
from models.client import Product
from dbservice import db
from datetime import datetime

product_router=APIRouter()


# Create a new product
@product_router.post("/", response_model=ProductResponse)
def create_product(product_request: ProductRequest):
    try:
        new_product = Product(**product_request.dict())
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        return new_product
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# Get all products
@product_router.get("/", response_model=list[ProductResponse])
def get_products():
    try:
        products = db.query(Product).all()
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Get a single product by ID
@product_router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int):
    try:
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Update a product
@product_router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product_update: ProductUpdate):
    try:
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        if product_update.productPrice:
            product.productPrice=product_update.productPrice

        if product_update.last_updated:
            product.last_updated=product_update.last_updated

        if product_update.productName:
            product.productName=product_update.productName

        db.commit()
        db.refresh(product)
        return product
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500)


# Delete a product
@product_router.delete("/{product_id}")
def delete_product(product_id: int):
    try:
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        db.delete(product)
        db.commit()
        return {"message": "Product deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))