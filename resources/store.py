import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores
from schemas import StoreSchema

blp = Blueprint("stores", __name__, description="Operations on stores")

@blp.route('/stores/<string:store_id>')
class StoreById(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
      try:
        return stores[store_id]
      except KeyError:
        abort(404, message="Store not found")

    def delete(self, store_id):
      try:
        del stores[store_id]
        return "", 204
      except KeyError:
          abort(404, message="Store not found") 

    @blp.response(200, StoreSchema)
    def put(self, store_id):
      store_data = request.get_json()

      if "name" not in store_data:
        abort(400, message="name is a required param")

      try:
        store = stores[store_id]
        store |= store_data
        return store
      except KeyError:
        abort(404, message="Store not found") 

@blp.route('/stores')
class Store(MethodView):
    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    def post(self, store_data):
      for store in stores.values():
        if store["name"] == store_data["name"]:
              abort(400, message="Store already exists")

      store_id = uuid.uuid4().hex
      store = {**store_data, "id": store_id}
      stores[store_id] = store
      return store, 201

    @blp.response(200, StoreSchema(many=True))
    def get(self):
      return stores.values()     
    
    