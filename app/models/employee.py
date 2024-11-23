from dbservice import relationship, Base, String, ForeignKey, Column, Integer, Boolean, datetime, DateTime


class Role(Base):
    __tablename__="roles"

    id=Column(Integer,primary_key=True,autoincrement=True)
    roleName=Column(String, nullable=False)
    company_id=Column(Integer, ForeignKey('companies.id'))


    #relationships
    employees=relationship('Employee',backref='employee_roles') 
    companyroles=relationship('Company', backref='adminrole', foreign_keys=[company_id])

class Employee(Base):
    __tablename__= 'employees'

    id=Column(Integer,primary_key=True,autoincrement=True)
    employee_name=Column(String(50) ,nullable=False)
    employee_email=Column(String(100) ,nullable=False , unique=True)
    national_id_number = Column(String(80), nullable=False, unique=True)
    password=Column(String(255), nullable=False, unique=True)
    branch_id=Column(Integer, ForeignKey('branches.id'))
    role_id=Column(Integer, ForeignKey('roles.id'),nullable=False)
    is_active=Column(Boolean, default=True)
    company_id=Column(Integer, ForeignKey('companies.id'), nullable=False)
    registration_date=Column(DateTime, default=datetime.utcnow)

    #Relationship
    # branch=relationship('Branch',backref='employees')
