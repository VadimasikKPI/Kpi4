from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any

from flask_restful import reqparse

from Singleton import Singleton
import requests
import time
from Specification import MaxPrice, MinPrice, PackageName



class PackageBuilder(ABC):
    @property
    @abstractmethod
    def pakage(self) -> None:
        pass
    @abstractmethod
    def extract_from_source(self) ->None:
        pass
    @abstractmethod
    def reformat(self) -> None:
        pass
    @abstractmethod
    def filter(self) -> None:
        pass


class ServiceOnePackageBuilder(PackageBuilder):
    def __init__(self) -> None:
        self.reset()
    def reset(self) -> None:
        self._pakage = ProgramPackage()
    def pakage(self) -> None:
        self._pakage = ProgramPackage()
    @property
    def pakage(self) -> ProgramPackage:
        product = self._pakage
        self.reset()
        return product
    def extract_from_source(self) ->None:
        self._pakage.set(requests.get('http://127.0.0.1:5001/search/').json())
    def reformat(self) -> None:
        pass
    def filter(self) -> None:
        self._pakage.filter()
class ServiceTwoPackageBuilder(PackageBuilder):
    def __init__(self) -> None:
        self.reset()
    def reset(self) -> None:
        self._pakage = ProgramPackage()
    @property
    def pakage(self) -> ProgramPackage:
        pakage = self._pakage
        self.reset()
        return pakage
    def extract_from_source(self) ->None:
        #self._pakage.set(requests.get('http://127.0.0.1:5002/price-list/').json())
        page = [0]
        page_n = 1
        while len(page) > 0:
            page = requests.get('http://127.0.0.1:5002/price-list?page=' + str(page_n)).json()

            page_n += 1
            self._pakage.pakages += page
    def reformat(self) -> None:
        full_pakages = []
        for row in self._pakage.pakages:
            full_pakages.append(requests.get('http://127.0.0.1:5002/details/'+str(row["packageid"])).json())
        self._pakage.set(full_pakages)
    def filter(self) -> None:
        self._pakage.filter()

class ProgramPackageBuilder(PackageBuilder):
    def __init__(self) -> None:
        self.reset()
        self.db = Singleton()
    def reset(self) -> None:
        self._pakage = ProgramPackage()
    @property
    def pakage(self) -> ProgramPackage:
        pakage = self._pakage
        self.reset()
        return pakage
    def extract_from_source(self) ->None:
        self._pakage.set(self._pakage.select_all_packages())
    def reformat(self) -> None:
        my_list = []
        for row in self.pakage.pakages:
            a = {"packageID": row[0], "name": row[1], "time": row[2], "price": str(row[3]),
                 "information": str(row[4])}
            my_list.append(a)
        self._pakage.set(my_list)
    def filter(self) -> None:
        self._pakage.filter()

class Director:
    def __init__(self) -> None:
        self._builder = None

    @property
    def builder(self) -> builder:
        return self._builder

    @builder.setter
    def builder(self, builder: builder) -> None:
        self._builder = builder

    def build_all_pakage(self) -> None:
        self.builder.extract_from_source()
        self.builder.reformat()
    def build_filtered_pakage(self) -> None:
        self.builder.extract_from_source()
        self.builder.reformat()
        self.builder.filter()
class ProgramPackage():
    def __init__(self):
        self.pakages = []
        self.filtered_pakages = []
        self.arg= {}
        self.conn = Singleton().conn
    def add(self, product: dict[str, Any]):
        self.pakages.append(product)
    def join(self, another_pakage):
        self.pakages += another_pakage.pakages
    def drop(self, id):
        del self.pakages[id]
    def set(self, pakages):
        self.pakages = pakages
    def select_all_packages(self):
        rows = []

        with self.conn.cursor() as cursor:
            cursor.execute('SELECT "packageid", "name", "time", "price", "information" FROM "package"')
            rows = cursor.fetchall()

        return rows
    def insert(self, args):
        with self.conn.cursor() as cursor:
            cursor.execute(
                '''INSERT INTO "cache" ("name", "time", "price", "information") VALUES('%s','%s','%s','%s')'''%((args["name"]), (args["time"]), int(args["price"]), (args["information"])))
        self.conn.commit()

        with self.conn.cursor() as cursor:
            cursor.execute('''INSERT INTO "package" ("name", "time", "price", "information") VALUES('%s','%s','%s','%s')'''%((args["name"]), (args["time"]), int(args["price"]), (args["information"])))
        self.conn.commit()
        with self.conn.cursor() as cursor:
            cursor.execute(
                '''SELECT p1."packageid", p1."name", p1."time", p1."price", p1."information" FROM "package" p1 ''')
            rows = cursor.fetchall()
        args = self.reform(rows[-1])

    def delete(self, id):
        with self.conn.cursor() as cursor:
            cursor.execute('DELETE FROM "package" WHERE "packageid"=%s'%id)
            cursor.execute('DELETE FROM "cache" WHERE "packageid"=%s'%id)
        self.conn.commit()

    def update(self, args):
        query_str = 'UPDATE Cache SET '
        for key, value in args.items():
            if key != 'packageid' and value != None:
                query_str += '"' + key + '"=' + "'" + str(value) + "',"
        query_str = query_str[0:-1]

        query_str += ' WHERE "packageid"=' +str(args["packageid"])
        with self.conn.cursor() as cursor:
            cursor.execute(query_str)
        self.conn.commit()

        query_str = 'UPDATE Package SET '
        for key, value in args.items():
            if key != 'packageid' and value != None:
                query_str += '"' + key + '"=' + "'" + str(value) + "',"
        query_str = query_str[0:-1]
        query_str += ' WHERE "packageid"=' + str(args["packageid"])
        with self.conn.cursor() as cursor:
            cursor.execute(query_str)
        self.conn.commit()

        with self.conn.cursor() as cursor:
            cursor.execute(
                '''SELECT p1."packageid", p1."name", p1."time", p1."price", p1."information" FROM "package" p1''')
            rows = cursor.fetchall()
        args = self.reform(rows[-1])

    def oldfilter(self, x):
        pakage_filter = MaxPrice() & MinPrice() & PackageName()
        if pakage_filter.is_satisfied_by(x, self.args):
            return x
        return None

    def filter(self):
        # product_filter = SaleType() & MaxPrice() & MinPrice() & ProductName()
        packages = []
        parser = reqparse.RequestParser()
        parser.add_argument("package_name")
        parser.add_argument("min_price")
        parser.add_argument("max_price")
        self.args = parser.parse_args()
        import multiprocessing
        self.conn = None
        t1 = time.time()
        with multiprocessing.Pool(4) as pool:
            self.pakages = pool.map(self.oldfilter, self.packages)
        print(time.time() - t1)
        t1 = time.time()
        self.packages = list(filter(None, self.packages))
        print(time.time() - t1)
        self.conn = Singleton().conn

    def reform(self, row):
        return {"packageID": row[0], "name": row[1], "time": row[2], "price": str(row[3]),
                "information": str(row[4])}
