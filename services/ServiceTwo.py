from flask import Flask
from flask_restful import Resource, Api, reqparse
import psycopg2





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

    def select_all_price(self, page):
        rows = []
        with self.conn.cursor() as cursor:
            cursor.execute('SELECT s1."packageid", s1."name",  s1."price",s1."time", s1."servicetwo" FROM "service" s1 LIMIT 5000 OFFSET '+str((page-1)*5000))
            rows = cursor.fetchall()
        return rows
    def select_all_information(self, i):
        rows = []
        with self.conn.cursor() as cursor:
            cursor.execute('SELECT s1."packageid", s1."name", s1."information", s1."price",s1."time", s1."servicetwo"  FROM "service" s1 WHERE s1."packageid"=%d'%i)
            rows = cursor.fetchall()
        return rows




class Prices(Resource):
    def get(self):
        db = Singleton()
        parser = reqparse.RequestParser()
        parser.add_argument("page")
        args = parser.parse_args()
        page = 1
        if args['page']:
            page = int(args['page'])
        all_packages = db.select_all_price(page)
        my_list = []
        for row in all_packages:
            a = {"packageid": row[0], "name": row[1],  "price": row[2], "time": row[3], "serviceTwo":row[4]}
            my_list.append(a)
        return my_list

class Information(Resource):
    def get(self, id):
        db = Singleton()
        all_packages = db.select_all_information(id)
        my_list = []
        for row in all_packages:
            a ={"packageid": row[0], "name": row[1],
                 "information": row[2], "price": row[3], "time": row[4], "serviceTwo":row[5]}
            my_list.append(a)

        return my_list[0]

if __name__ == "__main__":
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(Prices, '/price-list/')
    api.add_resource(Information, '/details/<int:id>')
    app.run(port=5002, debug=True)

