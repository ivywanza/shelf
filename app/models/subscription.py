from dbservice import Base, Integer, datetime, DateTime, Column, Float, String,relationship


class Package(Base):
    __tablename__="packages"

    id=Column(Integer,primary_key=True,autoincrement=True)
    package_name=Column(String,nullable=False)
    content=Column(String, nullable=False)
    start_date=Column(DateTime, default=datetime.utcnow)
    end_date= Column(DateTime, nullable=False)
    price= Column(Float(2), nullable=False)

    # relationship
    company=relationship('Company', backref="package")

