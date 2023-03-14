from marshmallow import Schema, fields


class ItemSchema(Schema):
    key = fields.Str(required=True)
    description = fields.Str(required=True)
    status = fields.Bool(required=True)


class ItemUpdateSchema(Schema):
    status = fields.Bool(required=True)
