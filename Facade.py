from flask_restful import reqparse
from PakageBuilder import Director, ProgramPackageBuilder, ServiceOnePackageBuilder, ServiceTwoPackageBuilder, ProgramPackage
from Singleton import Singleton
from Cache import CachePakage



class Facade:
    def __init__(self):
        self.director = Director()
        self.db = Singleton()
        self.parser = reqparse.RequestParser()
        self.empty_package = ProgramPackage()
        self.cache = CachePakage()
    def get_pakage(self):
        # director = Director()
        # builder = ProgramPackageBuilder()
        # self.director.builder = builder
        # self.director.build_filtered_pakage()
        # own = builder.pakage
        #
        # builder = ServiceOnePackageBuilder()
        # self.director.builder = builder
        # self.director.build_filtered_pakage()
        # serviceOne = builder.pakage
        #
        # builder = ServiceTwoPackageBuilder()
        # self.director.builder = builder
        # self.director.build_filtered_pakage()
        # serviceTwo = builder.pakage
        # own.join(serviceOne)
        # own.join(serviceTwo)
        return self.cache.get_cache()
    def insert(self):
        self.parser.add_argument("packageid")
        self.parser.add_argument("name")
        self.parser.add_argument("time")
        self.parser.add_argument("price")
        self.parser.add_argument("information")

        args = self.parser.parse_args()
        self.empty_package.insert(args)
    def delete(self):
        self.parser.add_argument("packageid")
        args = self.parser.parse_args()
        self.empty_package.delete(args["packageid"])
    def update(self):
        self.parser.add_argument("packageid")
        self.parser.add_argument("name")
        self.parser.add_argument("time")
        self.parser.add_argument("price")
        self.parser.add_argument("information")
        args = self.parser.parse_args()
        self.empty_package.update(args)
