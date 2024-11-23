from dbservice import Integer, String, relationship, Base, ForeignKey, Column, Float, Boolean


class ShelfType(Base):
    __tablename__= 'shelf_types'

    id=Column(Integer,primary_key=True,autoincrement=True)
    size=Column(String(80),nullable=False)
    description=Column(String(255))
    price=Column(Float(2),nullable=False)
    company_id=Column(Integer, ForeignKey('companies.id'), nullable=False)

    #relationship
    shelf = relationship('Shelf', backref='shelf_types')

class Shelf(Base):
    __tablename__ = 'shelves'

    id=Column(Integer,primary_key=True,autoincrement=True)
    account_number = Column(String(70), nullable=False, unique=True)
    is_occupied = Column(Boolean , default=False ,nullable=False)
    shelf_type_id = Column(Integer, ForeignKey("shelf_types.id"), nullable=False)
    #relationship
    
    # Payment=relationship('Payment' ,backref='shelves')
    client=relationship('Client', backref='shelves') 
    products=relationship('Product', backref="product_shelf" )