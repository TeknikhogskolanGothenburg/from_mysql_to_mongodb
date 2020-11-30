from mongo.base_document import Document, db


class Product(Document):
    collection = db.products


class Office(Document):
    collection = db.offices


class Employee(Document):
    collection = db.employees

class Customer(Document):
    collection = db.customers


class Order(Document):
    collection = db.orders