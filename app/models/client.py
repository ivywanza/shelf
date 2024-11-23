from dbservice import Base, Integer,Column, ForeignKey, DateTime, datetime, String, relationship, Float

class Product(Base):
    __tablename__="products"

    id=Column(Integer, primary_key=True,autoincrement=True)
    client_id=Column(Integer, ForeignKey('clients.id'), nullable=False)
    productName=Column(String,nullable=False)
    productPrice=Column(Float(2), nullable=False)
    stock_quantity=Column(Integer, nullable=False)
    shelf_id=Column(Integer, ForeignKey('shelves.id'))
    last_updated=Column(DateTime, default=datetime.utcnow)

class Client(Base):
    __tablename__ = 'clients'

    id=Column(Integer,primary_key=True,autoincrement=True)
    client_name = Column(String(100), nullable=False)
    client_email= Column(String(100), nullable=False, unique=True)
    phone_number=Column(String(20),unique=True)
    start_date= Column(DateTime, default=datetime.utcnow, nullable=False)
    shelf_id= Column(Integer, ForeignKey('shelves.id'))
    company_id = Column(Integer, ForeignKey('companies.id'))
    
    # relationship

    client_product=relationship('Product', backref='cl_products')
