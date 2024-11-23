from fastapi import FastAPI
from dbservice import Base, engine, db, event
from router import companies, subscription, employee, client, shelf,product, buyer,\
order
from models.employee import Role
from schemas import tags



app=FastAPI()

app.include_router(companies.company_router, prefix='/comapany', tags=[tags.Tags.COMPANY.value])
app.include_router(subscription.subscription_router, prefix='/subscription', tags=[tags.Tags.SUBSCRIPTION.value])
app.include_router(employee.employee_router, tags=[tags.Tags.EMPLOYEE.value])
app.include_router(client.client_router, prefix='/client', tags=[tags.Tags.CUSTOMER.value])
app.include_router(shelf.shelf_router, prefix='/shelf', tags=[tags.Tags.SHELF.value])
app.include_router(product.product_router, prefix='/product', tags=[tags.Tags.PRODUCTS.value])
app.include_router(buyer.buyer_router, prefix='/buyer', tags=[tags.Tags.BUYER.value])
app.include_router(buyer.buyer_router, prefix='/order', tags=[tags.Tags.ORDER.value])


@app.on_event("startup")
async def on_startup():
    Base.metadata.create_all(bind=engine)

    # Initialize roles
    # db = SessionLocal()
    try:
        initialize_roles()
    finally:
        db.close()
    # $2b$12$6yfE3clvZgZS1k6lTWwgfeoqRMS4uCCaBeZfEmc/qVBAgBi8eTR1W
@app.get("/")
def read_root():
    return {"message": "Welcome to my application"}

# db = SessionLocal()
def initialize_roles():
    existing_role = db.query(Role).filter(Role.roleName == "superadmin").first()
    if not existing_role:
        super_admin_role = Role(roleName="superadmin", company_id=None)
        db.add(super_admin_role)
        db.commit()

Base.metadata.create_all(engine)