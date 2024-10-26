from marshmallow import Schema, fields

class ItemSchema(Schema):
    id = fields.str(dump_only=True)
    name = fields.str(required=True)
    price = fields.Float(required=True)
    store_id = fields.str(required=True)

class ItemUpdateSchema(Schema):
    name = fields.str()
    price = fields.Float()

class StoreSchema(Schema):
    id = fields.str(dump_only=True)
    name = fields.str(required=True)