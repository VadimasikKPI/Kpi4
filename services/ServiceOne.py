from flask import Flask
from flask_restful import Resource, Api, reqparse
import psycopg2
import time
import random
from Specification import  MaxPrice, MinPrice, PackageName


class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
class Singleton(metaclass=SingletonMeta):
    def __init__(self):
        self.conn = psycopg2.connect(host="localhost", user="postgres", password="fanibo80", database="fotostudia", port="5432")

    def select_all_prod(self):
        rows = []
        with self.conn.cursor() as cursor:
            cursor.execute(
                'SELECT p1."packageid", p1."name", p1."time", p1."price", p1."information" FROM "package" p1 ')
            rows = cursor.fetchall()
        return rows




class Pakage(Resource):
    def get(self):
        db = Singleton()
        time.sleep(random.randint(20, 30))
        all_packages = db.select_all_prod()
        my_list = []
        for row in all_packages:
            a = {"packageID": row[0], "name": row[1], "time": row[2], "price": row[3],
                 "information": row[4]}
            my_list.append(a)
        all_packages.clear()

        package_filter = MaxPrice() & MinPrice() & PackageName()
        pakages = []
        parser = reqparse.RequestParser()
        parser.add_argument("name")
        parser.add_argument("min_price")
        parser.add_argument("max_price")
        args = parser.parse_args()
        for i in my_list:
            # print((i))
            if package_filter.is_satisfied_by(i, args):
                pakages.append(i)
        return pakages

if __name__ == "__main__":
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(Pakage, '/search/')
    app.run(port=5001, debug=True)
