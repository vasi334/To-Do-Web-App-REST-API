from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from db import db

from flask import jsonify

from schemas import ItemSchema, ItemUpdateSchema
from models import ItemModel

blp = Blueprint("items", __name__, description="Operations on items")


@blp.route("/item/<string:item_key>")
class ItemsChange(MethodView):
    @blp.arguments(ItemUpdateSchema)
    def put(self, item_data, item_key):
        # for i in items:
        #     if (i["key"] == item_key):
        #         i["status"] = item_data["status"]
        #         return i

        # return abort(404, message="Item not found.")
        item = ItemModel.query.filter_by(key=item_key).first()
        if item:
            item.status = item_data["status"]
        else:
            abort(500, message="An error occured while inserting the item.")

        db.session.add(item)
        db.session.commit()

        return {"message": "Item updated."}

    def delete(self, item_key):
        item = ItemModel.query.filter_by(key=item_key).first()
        if item:
            db.session.delete(item)
            db.session.commit()
            return {"message": "Item deleted"}
        else:
            return abort(404, message="Item not found.")


@blp.route("/item")
class Items(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        # return items
        return ItemModel.query.all()

    @blp.arguments(ItemSchema)
    @blp.response(200, ItemSchema)
    def post(self, item_data):
        # new_item = {"key": item_data["key"],
        #             "description": item_data["description"],
        #             "status": item_data["status"]}
        # items.append(new_item)
        new_item = ItemModel(**item_data)

        try:
            db.session.add(new_item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occured while inserting the item.")
        return new_item, 201


@blp.route("/itemsActive")
class ItemsActive(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        items_active = []
        all_items = ItemModel.query.all()
        for item in all_items:
            if (item.status):
                items_active.append(
                    {
                        "key": item.key,
                        "description": item.description,
                        "status": item.status
                    })

        return items_active


@blp.route("/itemsCompleted")
class ItemsCompleted(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        items_completed = []
        all_items = ItemModel.query.all()
        for item in all_items:
            if (not item.status):
                items_completed.append(
                    {
                        "key": item.key,
                        "description": item.description,
                        "status": item.status
                    })
        print(items_completed)
        return items_completed
