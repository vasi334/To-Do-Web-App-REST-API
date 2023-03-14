from db import db


class ItemModel(db.Model):
    __tablename__ = "items"

    key = db.Column(db.String(80), primary_key=True)
    description = db.Column(db.String(80), unique=False, nullable=False)
    status = db.Column(db.Boolean, unique=False, nullable=False)
