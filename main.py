import threading

from flask import Flask, request
from flask_restful import Api

from Singleton import Singleton
from Router import *
from Cache import CachePakage



if __name__ == "__main__":
    app = Flask(__name__)
    api = Api(app)
    cache = CachePakage()
    # cache.update()
    # threading.Timer(cache.time_to_update(), cache.update())
    @app.route("/get_pakages/", methods=['GET', 'POST', 'DELETE', 'PUT'])
    def get_pakages():
        post = PostHandler()
        get = GetHandler()
        delete = DeleteHandler()
        put = PutHandler()
        post.set_next(get).set_next(delete).set_next(put)
        return post.handle(request.method)
    app.run(debug=True, use_reloader=True)
    Singleton().conn.close()

