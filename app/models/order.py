from dbservice import relationship, Base, String, ForeignKey, Column, Integer, Boolean, datetime, DateTime, Float

class Order(Base):
    __tablename__="orders"

    id=Column(Integer,primary_key=True,autoincrement=True)
    order_number=Column(String, nullable=False)
    buyer_id=Column(Integer, ForeignKey('buyers.id'))
    product_id=Column(Integer, ForeignKey('products.id'))
    quantity=Column(Integer, nullable=False)
    totalPrice=Column(Float(2), nullable=False)
    status_id=Column(Integer, ForeignKey('status.id'))

    # relationship
    products=relationship('Product', backref='ordered_products')
    status=relationship('Status', backref='order_status')
