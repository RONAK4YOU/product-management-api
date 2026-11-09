"""Database-backed Product model and query helpers."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    price = db.Column(db.Float, nullable=False)
    available = db.Column(db.Boolean, nullable=False, default=True)
    category = db.Column(db.String(80), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "available": self.available,
            "category": self.category,
        }

    def deserialize(self, data):
        for field in ("name", "description", "price", "available", "category"):
            if field in data:
                setattr(self, field, data[field])
        return self

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def update(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find(cls, product_id):
        return cls.query.get(product_id)

    @classmethod
    def all(cls):
        return cls.query.order_by(cls.id).all()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter(cls.name.ilike(f"%{name}%")).order_by(cls.id).all()

    @classmethod
    def find_by_category(cls, category):
        return cls.query.filter(cls.category.ilike(category)).order_by(cls.id).all()

    @classmethod
    def find_by_availability(cls, available):
        return cls.query.filter_by(available=available).order_by(cls.id).all()
