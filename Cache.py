import datetime
import threading
import multiprocessing as mp

from flask_restful import reqparse

from Singleton import Singleton
from PakageBuilder import Director, ServiceOnePackageBuilder, ServiceTwoPackageBuilder, ProgramPackageBuilder
from psycopg2.extras import execute_values

class SingletonCache(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
class CachePakage(metaclass=SingletonCache):
    def __init__(self):
        self.own_cache = []
        self.service_1_cache = []
        self.service_2_cache = []
    def time_to_update(self):
        dt = datetime.datetime.now()
        tomorrow = dt + datetime.timedelta(days=1)
        return (datetime.datetime.combine(tomorrow, datetime.time.min) - dt).seconds
    def own_prod(self, q):
        director = Director()
        builder = ProgramPackageBuilder()
        director.builder = builder
        director.build_all_pakage()
        own = builder.pakage
        q.put(own.pakages)
    def serv1_prod(self, q):
        director = Director()
        builder = ServiceOnePackageBuilder()
        director.builder = builder
        director.build_all_pakage()
        serv1 = builder.pakage

        q.put(serv1.pakages)
    def serv2_prod(self, q):
        director = Director()
        builder = ServiceTwoPackageBuilder()
        director.builder = builder
        director.build_all_pakage()
        serv2 = builder.pakage

        q.put(serv2.pakages)
    def update(self):

        conn = Singleton().conn
        q1 = mp.Queue()
        p1 = mp.Process(target=self.own_prod, args=(q1,))

        q2 = mp.Queue()
        p2 = mp.Process(target=self.serv1_prod, args=(q2,))

        q3 = mp.Queue()
        p3 = mp.Process(target=self.serv2_prod, args=(q3,))
        p1.start()
        p2.start()
        p3.start()
        self.own_cache = q1.get()
        self.service_1_cache = q2.get()
        self.service_2_cache = q3.get()
        with conn.cursor() as cursor:
            cursor.execute('TRUNCATE cache')
            execute_values(cursor,
                           '''INSERT INTO "cache" ("name", "time", "price", "information") VALUES %s''',
                            [(args["name"], args["time"], int(args["price"]), args["information"]) for args in self.own_cache + self.service_1_cache + self.service_2_cache])
        conn.commit()
        p1.join()
        p2.join()
        p3.join()

        director = Director()
        builder = ProgramPackageBuilder()
        director.builder = builder
        director.build_all_pakage()
        own = builder.pakage
        self.own_cache = own.pakages

        builder = ServiceOnePackageBuilder()
        director.builder = builder
        director.build_all_pakage()
        service1 = builder.pakage
        self.service_1_cache = service1.pakages

        builder = ServiceTwoPackageBuilder()
        director.builder = builder
        director.build_all_pakage()
        service2 = builder.pakage
        self.service_2_cache = service2.pakages
        timer = threading.Timer(self.time_to_update(), self.update)
        timer.start()
    def get_cache(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name")
        parser.add_argument("min_price")
        parser.add_argument("max_price")
        args = parser.parse_args()
        parse_str = '''SELECT * FROM Cache '''
        filt_opt = []
        if args['name']:
            filt_opt.append(['"name"=', args['name']])
        if args['min_price']:
            filt_opt.append(['"price">', args['min_price']])
        if args['max_price']:
            filt_opt.append(['"price"<', args['max_price']])
        if len(filt_opt)>0:
            parse_str+='WHERE '
        for i in range(len(filt_opt)):
            parse_str += filt_opt[i][0]+"'"+ filt_opt[i][1] + "'"
            if i+1 < len(filt_opt):
                parse_str+=' AND '
        conn = Singleton().conn
        with conn.cursor() as cursor:
            cursor.execute(parse_str)
            rows = cursor.fetchall()
        result = []
        for row in rows:
            a = {"packageID": row[0], "name": row[1], "time": row[2], "price": row[3],
                 "information": row[4]}
            result.append(a)
        return result