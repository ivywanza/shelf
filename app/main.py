from app.routers import company_router, subscription_router
from fastapi import FastAPI

app=FastAPI()

app.include_router(company_router, prefix='/comapany')
app.include_router(subscription_router, prefix='/subscription')