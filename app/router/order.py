from fastapi import APIRouter, HTTPException
from schemas.order import OrderRequest,OrderResponse,OrderUpdate
from dbservice import db
from models.order import Order

order_router=APIRouter()


# Create an Order
@order_router.post("/", response_model=OrderResponse)
def create_order(order: OrderRequest):
    try:
        new_order = Order(**order.dict())
        db.add(new_order)
        db.commit()
        db.refresh(new_order)
        return new_order
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating order: {e}")

# Get All Orders
@order_router.get("/", response_model=list[OrderResponse])
def get_all_orders():
    try:
        return db.query(Order).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching orders: {e}")

# Get an Order by ID
@order_router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int):
    try:
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return order
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching order: {e}")

# Update an Order
@order_router.put("/{order_id}", response_model=OrderResponse)
def update_order(order_id: int, updated_order: OrderUpdate):
    try:
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        if updated_order.product_id:
            order.product_id=updated_order.product_id

        if updated_order.quantity:
            order.quantity=updated_order.quantity

        if updated_order.totalPrice:
            order.totalPrice=updated_order.totalPrice

        if updated_order.status_id:
            order.status_id=updated_order.status_id

        db.commit()
        db.refresh(order)
        return order
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating order: {e}")

# Delete an Order
@order_router.delete("/{order_id}")
def delete_order(order_id: int):
    try:
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        db.delete(order)
        db.commit()
        return {"detail": "Order deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting order: {e}")