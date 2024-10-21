from dbservice import Base, Integer, datetime, Datetime, Column, Float, String


class Package(Base):
    __tablename__="packages"

    id=Column(Integer,primary_key=True,autoincrement=True)
    package_name=Column(String,nullable=False)
    content=Column(String, nullable=False)
    start_date=Column(Datetime, default=datetime.utcnow)
    end_date= Column(Datetime, nullable=False)
    price= Column(Float(2), nullable=False)

