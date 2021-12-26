from .models import Package, Client, Order
from ariadne import convert_kwargs_to_snake_case

def listPackages_resolver(obj, info):
    try:
        packages = [package.to_dict() for package in Package.query.limit(5000)]

        print(packages)
        payload = {
            "success": True,
            "packages": packages
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload


@convert_kwargs_to_snake_case
def getPackage_resolver(obj, info, id):
    try:
        package = Package.query.get(id)
        print(package.to_dict())
        payload = {
            "success": True,
            "package": package.to_dict()
        }
    except AttributeError:
        payload = {
            "success": False,
            "errors": ["Package item matching {id} not found"]
        }
    return payload

def listClients_resolver(obj, info):
    try:
        clients = [client.to_dict() for client in Client.query.all()]

        print(clients)
        payload = {
            "success": True,
            "clients": clients
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload

@convert_kwargs_to_snake_case
def getClient_resolver(obj, info, id):
    try:
        client = Client.query.get(id)
        print(client.to_dict())
        payload = {
            "success": True,
            "client": client.to_dict()
        }
    except AttributeError:
        payload = {
            "success": False,
            "errors": ["Client item matching {id} not found"]
        }
    return payload


def listOrders_resolver(obj, info):
    try:
        orders = [order.to_dict() for order in Order.query.all()]
        payload = {
            "success": True,
            "orders": orders
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload


@convert_kwargs_to_snake_case
def getOrder_resolver(obj, info, id):
    try:
        order = Order.query.get(id)

        payload = {
            "success": True,
            "order": order.to_dict()
        }
    except AttributeError:
        payload = {
            "success": False,
            "errors": ["Order item matching {id} not found"]
        }
    return payload
