from dbservice import Integer, Column, Base, String, datetime, DateTime, ForeignKey, relationship, Boolean


class Company(Base):
    __tablename__="companies"

    id=Column(Integer,primary_key=True,autoincrement=True)
    company_name=Column(String, nullable=False)
    company_email=Column(String(80), nullable=False, unique=True)
    phone_number=Column(String(20),nullable=False, unique=True)
    company_password = Column(String, nullable=False)
    company_location = Column(String, nullable=True)
    registration_date = Column(DateTime, default=datetime.utcnow)
    role_id =  Column(Integer, ForeignKey('roles.id'))
    package_id = Column(Integer, ForeignKey('packages.id'))
    is_active=Column(Boolean, default=True)

    # role=Column(Enum(UserRole),default=UserRole.SUPERIORADMIN)
    
    # relationships
    # package = relationship("Package", backref="company_subscription")
    employee = relationship('Employee', backref="company_employees")
    customer = relationship('Client', backref='company_client')
    role = relationship("Role", backref='company_role', foreign_keys=[role_id])
    branch = relationship('Branch', backref='company_branches')
    shelf_type=relationship('ShelfType', backref='company_shelfTypes')
    status=relationship('Status', backref="company_status")
    # product = relationship('Product', backref='company_products')
    # payment_method = relationship('CustomerToCompanyPaymentMethod', backref='company_customer_payment')
    # sales = relationship('Sale', backref='company_sale')
    # payments = relationship('Payment', backref='company_payments')

class Status(Base):
    __tablename__="status"

    id=Column(Integer,primary_key=True,autoincrement=True)
    name=Column(String,nullable=False)
    company_id=Column(Integer, ForeignKey('companies.id'), nullable=False)
    

    # relationship
    # branch=relationship('Branch', backref='branch_status')
    # employee=relationship('Employee', backref='employee_status')
    # company_status=relationship('Company' , backref='company')


class Branch(Base):
    __tablename__='branches'

    id=Column(Integer,primary_key=True,autoincrement=True)
    branch_location=Column(String(100), nullable=False)
    branch_name = Column(String(80), nullable=False)
    # status_id=Column(Integer,ForeignKey('status.id'), nullable=False)
    company_id=Column(Integer,ForeignKey('companies.id'), nullable=False)
    registration_date=Column(DateTime, default=datetime.utcnow)
    is_active=Column(Boolean, default=True)
    #relationships
    employee=relationship('Employee', backref='branches_employees')