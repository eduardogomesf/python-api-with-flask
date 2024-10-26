import uuid
from flask import Flask, request
from flask_smorest import abort
from db import items, stores

app = Flask(__name__)

# Stores
@app.get("/stores")
def get_stores():
    return { "stores": list(stores.values()) }

@app.post("/stores")
def create_store():
    store_data = request.get_json()

    if "name" not in store_data:
      abort(400, message="name is a required param")

    for store in stores.values():
       if store["name"] == store_data["name"]:
            abort(400, message="Store already exists")

    store_id = uuid.uuid4().hex
    store = {**store_data, "id": store_id}
    stores[store_id] = store
    return store, 201

@app.get("/stores/<string:store_id>")
def get_store(store_id):
    try:
      return stores[store_id]
    except KeyError:
      abort(404, message="Store not found")

@app.delete("/stores/<string:store_id>")
def delete_store(store_id):
  try:
     del stores[store_id]
     return "", 204
  except KeyError:
      abort(404, message="Store not found")

@app.put("/stores/<string:store_id>")
def update_store(store_id):
  store_data = request.get_json()

  if "name" not in store_data:
      abort(400, message="name is a required param")

  try:
     store = stores[store_id]
     store |= store_data

     return store
  except KeyError:
     abort(404, message="Store not found")
    

# Items
@app.post("/items")
def create_item():
    item_data = request.get_json()

    if(
       "price" not in item_data
       or "store_id" not in item_data
       or "name" not in item_data
    ):
        abort(400, message="price, store_id and name are required parameteres")

    if item_data["store_id"] not in stores:
      abort(404, message="Store not found")

    for item in items.values():
        if item["name"] == item_data["name"] and item["store_id"] == item_data["store_id"]:
            abort(400, message="Item already exists")
    
    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id}
    items[item_id] = item

    return item, 201
    
@app.get("/items")
def get_all_items():
  return { "items": list(items.values()) }

@app.get("/items/<string:item_id>")
def get_item(item_id):
  try:
    return items[item_id]
  except KeyError:
    abort(404, message="Item not found")

@app.delete("/items/<string:item_id>")
def delete_item(item_id):
  try:
     del items[item_id]
     return "", 204
  except KeyError:
      abort(404, message="Item not found")

@app.put("/items/<string:item_id>")
def update_item(item_id):
  item_data = request.get_json()

  if "name" not in item_data or "price" not in item_data:
      abort(400, message="name and store_id are required params")

  try:
     item = items[item_id]
     item |= item_data

     return item
  except KeyError:
     abort(404, message="Item not found")
    
      


