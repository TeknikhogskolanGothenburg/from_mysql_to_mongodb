from sqlalchemy import Column, DECIMAL, Date, ForeignKey, Integer, SmallInteger, String, Text
from sqlalchemy.dialects.mysql import MEDIUMBLOB, MEDIUMTEXT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Office(Base):
    __tablename__ = 'offices'

    officeCode = Column(String(10), primary_key=True)
    city = Column(String(50), nullable=False)
    phone = Column(String(50), nullable=False)
    addressLine1 = Column(String(50), nullable=False)
    addressLine2 = Column(String(50))
    state = Column(String(50))
    country = Column(String(50), nullable=False)
    postalCode = Column(String(15), nullable=False)
    territory = Column(String(10), nullable=False)


class Productline(Base):
    __tablename__ = 'productlines'

    productLine = Column(String(50), primary_key=True)
    textDescription = Column(String(4000))
    htmlDescription = Column(MEDIUMTEXT)
    image = Column(MEDIUMBLOB)


class Employee(Base):
    __tablename__ = 'employees'

    employeeNumber = Column(Integer, primary_key=True)
    lastName = Column(String(50), nullable=False)
    firstName = Column(String(50), nullable=False)
    extension = Column(String(10), nullable=False)
    email = Column(String(100), nullable=False)
    officeCode = Column(ForeignKey('offices.officeCode'), nullable=False, index=True)
    reportsTo = Column(ForeignKey('employees.employeeNumber'), index=True)
    jobTitle = Column(String(50), nullable=False)

    office = relationship('Office')
    parent = relationship('Employee', remote_side=[employeeNumber])


class Product(Base):
    __tablename__ = 'products'

    productCode = Column(String(15), primary_key=True)
    productName = Column(String(70), nullable=False)
    productLine = Column(ForeignKey('productlines.productLine'), nullable=False, index=True)
    productScale = Column(String(10), nullable=False)
    productVendor = Column(String(50), nullable=False)
    productDescription = Column(Text, nullable=False)
    quantityInStock = Column(SmallInteger, nullable=False)
    buyPrice = Column(DECIMAL(10, 2), nullable=False)
    MSRP = Column(DECIMAL(10, 2), nullable=False)

    productline = relationship('Productline')


class Customer(Base):
    __tablename__ = 'customers'

    customerNumber = Column(Integer, primary_key=True)
    customerName = Column(String(50), nullable=False)
    contactLastName = Column(String(50), nullable=False)
    contactFirstName = Column(String(50), nullable=False)
    phone = Column(String(50), nullable=False)
    addressLine1 = Column(String(50), nullable=False)
    addressLine2 = Column(String(50))
    city = Column(String(50), nullable=False)
    state = Column(String(50))
    postalCode = Column(String(15))
    country = Column(String(50), nullable=False)
    salesRepEmployeeNumber = Column(ForeignKey('employees.employeeNumber'), index=True)
    creditLimit = Column(DECIMAL(10, 2))

    employee = relationship('Employee')
    payments = relationship('Payment')


class Order(Base):
    __tablename__ = 'orders'

    orderNumber = Column(Integer, primary_key=True)
    orderDate = Column(Date, nullable=False)
    requiredDate = Column(Date, nullable=False)
    shippedDate = Column(Date)
    status = Column(String(15), nullable=False)
    comments = Column(Text)
    customerNumber = Column(ForeignKey('customers.customerNumber'), nullable=False, index=True)

    customer = relationship('Customer')
    orderdetail = relationship('Orderdetail')


class Payment(Base):
    __tablename__ = 'payments'

    customerNumber = Column(ForeignKey('customers.customerNumber'), primary_key=True, nullable=False)
    checkNumber = Column(String(50), primary_key=True, nullable=False)
    paymentDate = Column(Date, nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)

    customer = relationship('Customer')


class Orderdetail(Base):
    __tablename__ = 'orderdetails'

    orderNumber = Column(ForeignKey('orders.orderNumber'), primary_key=True, nullable=False)
    productCode = Column(ForeignKey('products.productCode'), primary_key=True, nullable=False, index=True)
    quantityOrdered = Column(Integer, nullable=False)
    priceEach = Column(DECIMAL(10, 2), nullable=False)
    orderLineNumber = Column(SmallInteger, nullable=False)

    order = relationship('Order')
    product = relationship('Product')
