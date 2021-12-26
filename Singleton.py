import psycopg2
from config import *

class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
class Singleton(metaclass=SingletonMeta):
    def __init__(self):
        self.conn = psycopg2.connect(host=host, user=user, password=password, database=db_name, port="5432")
