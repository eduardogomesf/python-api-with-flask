import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import items, stores
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("items", __name__, description="Operations on items")

@blp.route('/items/<string:store_id>')
class StoreById(MethodView):
    def get(self, item_id):
      try:
        return items[item_id]
      except KeyError:
        abort(404, message="Item not found")

    def delete(self, item_id):
      try:
        del items[item_id]
        return "", 204
      except KeyError:
          abort(404, message="Item not found")

    @blp.arguments(ItemUpdateSchema)
    def put(self, item_data, item_id):
      try:
        item = items[item_id]
        item |= item_data

        return item
      except KeyError:
        abort(404, message="Item not found")

@blp.route('/items')
class Store(MethodView):
    @blp.arguments(ItemSchema)
    def post(self, item_data):
      if item_data["store_id"] not in stores:
        abort(404, message="Store not found")

      for item in items.values():
          if item["name"] == item_data["name"] and item["store_id"] == item_data["store_id"]:
              abort(400, message="Item already exists")
      
      item_id = uuid.uuid4().hex
      item = {**item_data, "id": item_id}
      items[item_id] = item

      return item, 201

    def get(self):
      return { "items": list(items.values()) }     
    
    