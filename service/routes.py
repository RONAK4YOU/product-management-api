"""Flask application and REST endpoints for products."""
from flask import Flask, jsonify, render_template, request
from service.models import Product, db


def create_app(test_config=None):
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.config.update(
        SQLALCHEMY_DATABASE_URI="sqlite:///products.sqlite3",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JSON_SORT_KEYS=False,
    )
    if test_config:
        app.config.update(test_config)
    db.init_app(app)
    with app.app_context():
        db.create_all()

    @app.get("/")
    def home():
        return render_template("index.html")

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"})

    @app.post("/products")
    def create_product():
        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json"}), 415
        data = request.get_json(silent=True) or {}
        required = ("name", "description", "price", "available", "category")
        if not all(field in data for field in required):
            return jsonify({"error": "name, description, price, available, and category are required"}), 400
        try:
            product = Product(
                name=str(data["name"]),
                description=str(data["description"]),
                price=float(data["price"]),
                available=data["available"] if isinstance(data["available"], bool) else str(data["available"]).lower() == "true",
                category=str(data["category"]),
            ).create()
        except (TypeError, ValueError):
            return jsonify({"error": "Invalid product data"}), 400
        return jsonify(product.serialize()), 201

    # READ: look up the requested Product by ID.
    @app.get("/products/<int:product_id>")
    def read_product(product_id):
        product = Product.find(product_id)
        if product is None:
            return jsonify({"error": "Product not found"}), 404
        return jsonify(product.serialize()), 200

    # UPDATE: require JSON, update the found Product, persist, then serialize it.
    @app.put("/products/<int:product_id>")
    def update_product(product_id):
        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json"}), 415
        product = Product.find(product_id)
        if product is None:
            return jsonify({"error": "Product not found"}), 404
        data = request.get_json(silent=True) or {}
        try:
            if "available" in data and not isinstance(data["available"], bool):
                data["available"] = str(data["available"]).lower() == "true"
            if "price" in data:
                data["price"] = float(data["price"])
            product.deserialize(data).update()
        except (TypeError, ValueError):
            db.session.rollback()
            return jsonify({"error": "Invalid product data"}), 400
        return jsonify(product.serialize()), 200

    # DELETE: return an empty 204 response after successful deletion.
    @app.delete("/products/<int:product_id>")
    def delete_product(product_id):
        product = Product.find(product_id)
        if product is None:
            return jsonify({"error": "Product not found"}), 404
        product.delete()
        return "", 204

    # LIST ALL and explicit name, category, and availability searches.
    @app.get("/products")
    def list_products():
        name = request.args.get("name")
        category = request.args.get("category")
        raw_available = request.args.get("available")
        if raw_available is not None and raw_available.lower() not in ("true", "false"):
            return jsonify({"error": "available must be true or false"}), 400
        if name is not None:
            products = Product.find_by_name(name)
        elif category is not None:
            products = Product.find_by_category(category)
        elif raw_available is not None:
            available = raw_available.lower() == "true"
            products = Product.find_by_availability(available)
        else:
            products = Product.all()
        serialized = [product.serialize() for product in products]
        return jsonify({"products": serialized, "count": len(serialized)}), 200

    return app


app = create_app()
