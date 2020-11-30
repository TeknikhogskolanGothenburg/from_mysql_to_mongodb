import datetime

from mysql_db.db import session
from mysql_db.models import Product, Office, Employee, Customer, Order
import mongo.mongo_models as mm

def fix_products():
    products = session.query(Product).all()
    for product in products:
        as_dict = product.__dict__
        as_dict['buyPrice'] = float(as_dict['buyPrice'])
        as_dict['MSRP'] = float(as_dict['MSRP'])
        as_dict['productline'] = product.productline.__dict__
        del as_dict['_sa_instance_state']
        del as_dict['productline']['_sa_instance_state']

        as_dict['productline'] = {key: value for key, value in as_dict['productline'].items() if value is not None}

        mongo_product =mm.Product(as_dict)
        mongo_product.save()


def fix_offises():
    offices = session.query(Office).all()
    for office in offices:
        as_dict = office.__dict__
        as_dict = {key: value for key, value in as_dict.items() if value is not None}
        del as_dict['_sa_instance_state']
        mongo_office = mm.Office(as_dict)
        mongo_office.save()


def fix_employees():
    employees = session.query(Employee).all()
    for employee in employees:
        as_dict = employee.__dict__
        as_dict['officeId'] = mm.Office.find(officeCode=employee.officeCode).first_or_none()._id
        del as_dict['officeCode']
        del as_dict['_sa_instance_state']
        if as_dict['reportsTo'] is None:
            del as_dict['reportsTo']
        mongo_employee = mm.Employee(as_dict)

        mongo_employee.save()

    employees = mm.Employee.all()
    for employee in employees:
        if hasattr(employee, 'reportsTo'):
            employee.reportsTo = mm.Employee.find(employeeNumber=employee.reportsTo).first_or_none()._id
            employee.save()


def fix_customers():
    customers = session.query(Customer).all()
    for customer in customers:
        as_dict = customer.__dict__
        as_dict = {key:value for key, value in as_dict.items() if value is not None}
        if 'salesRepEmployeeNumber' in as_dict:
            as_dict['salesRepEmployeeNumber'] = mm.Employee.find(employeeNumber=as_dict['salesRepEmployeeNumber']).first_or_none()._id
        if 'creditLimit' in as_dict:
            as_dict['creditLimit'] = float(as_dict['creditLimit'])
        del as_dict['_sa_instance_state']
        payments = []
        for payment in customer.payments:
            payments.append({
                'amount': float(payment.amount),
                'checkNumber': payment.checkNumber,
                'paymentDate': datetime.datetime(payment.paymentDate.year, payment.paymentDate.month, payment.paymentDate.day)
            })
        as_dict['payments'] = payments

        mongo_customer = mm.Customer(as_dict)
        mongo_customer.save()


def fix_orders():
    orders = session.query(Order).all()
    for order in orders:
        as_dict = order.__dict__
        as_dict['orderDate'] = datetime.datetime(order.orderDate.year, order.orderDate.month, order.orderDate.day)
        as_dict['requiredDate'] = datetime.datetime(order.requiredDate.year, order.requiredDate.month, order.requiredDate.day)
        if order.shippedDate is not None:
            as_dict['shippedDate'] = datetime.datetime(order.shippedDate.year, order.shippedDate.month, order.shippedDate.day)
        else:
            del as_dict['shippedDate']
        if order.comments is None:
            del as_dict['comments']
        as_dict['customerId'] = mm.Customer.find(customerNumber=order.customerNumber).first_or_none()._id
        orderdetails = []
        for orderdetail in order.orderdetail:
            order_detail_dict = orderdetail.__dict__
            orderdetails.append({
                'productId': mm.Product.find(productCode=orderdetail.productCode).first_or_none()._id,
                'orderLineNumber': orderdetail.orderLineNumber,
                'quantityOrdered': orderdetail.quantityOrdered,
                'priceEach': float(orderdetail.priceEach)
            })
        as_dict['orderdetail'] = orderdetails

        del as_dict['_sa_instance_state']
        mongo_order = mm.Order(as_dict)
        mongo_order.save()


def clean_orders():
    orders = mm.Order.all()
    for order in orders:
        order.delete_field('customerNumber')



def main():
    #fix_products()
    #fix_offises()
    #fix_employees()
    #fix_customers()
    #fix_orders()
    clean_orders()

if __name__ == '__main__':
    main()
