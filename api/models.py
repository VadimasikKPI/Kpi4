from app import db

class Package(db.Model):
    packageid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    time = db.Column(db.Integer)
    price = db.Column(db.Integer)
    information = db.Column(db.String)
    def to_dict(self):
        return {
            'packageid': self.packageid,
            'name': self.name,
            'time': self.time,
            'price': self.price,
            'information': self.information
        }

class Client(db.Model):
    clientid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    number = db.Column(db.String)
    email = db.Column(db.String)
    def to_dict(self):
        return {
            "clientid": self.clientid,
            "name": self.name,
            "number": self.number,
            "email": self.email
        }

class Order(db.Model):
    orderid = db.Column(db.Integer, primary_key=True)
    clientid = db.Column(db.Integer)
    packageid = db.Column(db.Integer)
    def to_dict(self):
        return {
            'orderid': self.orderid,
            'clientid': self.clientid,
            'packageid': self.packageid
        }