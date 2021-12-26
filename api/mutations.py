from ariadne import convert_kwargs_to_snake_case
from api import db
from api.models import Package, Client, Order

def create_package_resolver(obj, info, name, time, price ,information):
    try:
        package = Package(name=name, time=time, price=price, information=information)
        db.session.add(package)
        db.session.commit()
        payload = {
            "success": True,
            "package": package.to_dict()
        }
    except AttributeError:
        payload = {
            "success": False,
            "errors": ["Package item attribute is not correct"]
        }
    return payload

@convert_kwargs_to_snake_case
def update_package_resolver(obj, info, packageid, name, price, time, information):
    try:
        package = Package.query.get(packageid)
        if package:
            package.name = name
            package.price = price
            package.time = time
            package.information = information
        db.session.add(package)
        db.session.commit()
        payload = {
        "success": True,
        "package": package.to_dict()
        }
    except AttributeError:
        payload = {
        "success": False,
        "errors": ["Not Found"]
        }
    return payload

@convert_kwargs_to_snake_case
def delete_package_resolver(obj, info, packageid):
    try:
        package = Package.query.get(packageid)
        db.session.delete(package)
        db.session.commit()
        payload = {
            "success": True,
            "package": package.to_dict()
        }
    except AttributeError:
        payload = {
            "success": False,
            "errors": ["Not Found"]
        }
    return payload

def create_client_resolver(obj, info, name, number, email):
    try:
        client = Client(name=name, number=number, email=email)
        db.session.add(client)
        db.session.commit()
        payload = {
            "success": True,
            "client": client.to_dict()
        }
    except AttributeError:
        payload = {
            "success": False,
            "errors": ["Client item attribute is not correct"]
        }
    return payload

@convert_kwargs_to_snake_case
def update_client_resolver(obj, info, clientid, name, number, email):
    try:
        client = Client.query.get(clientid)
        if client:
            client.name = name
            client.number = number
            client.email = email
        db.session.add(client)
        db.session.commit()
        payload = {
        "success": True,
        "client": client.to_dict()
        }
    except AttributeError:
        payload = {
        "success": False,
        "errors": ["Not Found"]
        }
    return payload

@convert_kwargs_to_snake_case
def delete_client_resolver(obj, info, clientid):
    try:
        client = Client.query.get(clientid)
        db.session.delete(client)
        db.session.commit()
        payload = {
            "success": True,
            "client": client.to_dict()
        }
    except AttributeError:
        payload = {
            "success": False,
            "errors": ["Not Found"]
        }
    return payload

def create_order_resolver(obj, info, clientid, packageid):
    try:
        order = Order(clientid=clientid, packageid=packageid)
        db.session.add(order)
        db.session.commit()
        payload = {
            "success": True,
            "order": order.to_dict()
        }
    except AttributeError:
        payload = {
            "success": False,
            "errors": ["Order item attribute is not correct"]
        }
    return payload

@convert_kwargs_to_snake_case
def update_order_resolver(obj, info, orderid, clientid, packageid):
    try:
        order = Order.query.get(orderid)
        if order:
            order.clientid = clientid
            order.packageid = packageid
        db.session.add(order)
        db.session.commit()
        payload = {
        "success": True,
        "order": order.to_dict()
        }
    except AttributeError:
        payload = {
        "success": False,
        "errors": ["Not Found"]
        }
    return payload

@convert_kwargs_to_snake_case
def delete_order_resolver(obj, info, orderid):
    try:
        order = Order.query.get(orderid)
        db.session.delete(order)
        db.session.commit()
        payload = {
            "success": True,
            "order": order.to_dict()
        }
    except AttributeError:
        payload = {
            "success": False,
            "errors": ["Not Found"]
        }
    return payload