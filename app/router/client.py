from dbservice import db
from models.client import Client
from schemas.client import ClientRequest,ClientResponse, ClientUpdate
from fastapi import APIRouter, HTTPException
from schemas import tags

client_router=APIRouter()

# register client
@client_router.post('/register')
def register_client(client: ClientRequest):
    try:
        existing_client=db.query(Client).filter(Client.client_email==client.client_email).first()
        if existing_client:
            raise HTTPException(status_code=409, detail="client with that email already exists")
        new_client=Client(
            client_name=client.client_name,
            client_email=client.client_email,
            phone_number=client.phone_number,
            shelf_id=client.shelf_id,
            company_id=client.company_id
        )
        db.add(new_client)
        db.commit()
        db.refresh(new_client)

        return {"message":"client registered successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}")
    
# get all company clients
@client_router.get('/fetch_all/{company_id}', response_model=list[ClientResponse])
def get_all_clients(company_id: int):
    try:
        clients= db.query(Client).filter(Client.company_id==company_id).all()
        return clients
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}")
    
# update client details
@client_router.put('/update/{client_id}')
def update_client_details(client_id: int, client_detail: ClientUpdate):
    try:
        client = db.query(Client).filter(Client.id==client_id).first()
        if client is None:
            raise HTTPException(status_code=404, detail="client does not exist")
        
        if client_detail.client_email:
            client.client_email=client_detail.client_email
        
        if client_detail.phone_number:
            client.phone_number=client_detail.phone_number

        if client_detail.shelf_id:
            client.shelf_id=client_detail.shelf_id

        db.commit()
        
        return {"messaga":"client details updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}")
    

