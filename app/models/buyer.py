from dbservice import relationship, Base, String, ForeignKey, Column, Integer, Boolean, datetime, DateTime

class Buyer(Base):
    __tablename__="buyers"

    id=Column(Integer,primary_key=True,autoincrement=True)
    user_name = Column(String(100), nullable=False, unique=True)
    buyer_email= Column(String(100), nullable=False, unique=True)
    phone_number=Column(String(20),unique=True)
    registration_date= Column(DateTime, default=datetime.utcnow, nullable=False)

    # relationship
    orders=relationship('Order', backref="buyer_orders")
