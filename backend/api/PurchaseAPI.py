from flask_restful import Resource, fields, marshal_with, reqparse
from flask_security import roles_accepted,auth_required, current_user
from flask import jsonify, request
from application.db import Product, ShoppingCart, Purchase
from application.db import db
from application.validation import NotFoundError, NotGivenError
from uuid import uuid4
from datetime import datetime
from application.cache import cache

purchase_fields = {
    "id": fields.Integer,
    "user_id": fields.Integer,
    "order_id": fields.String,
    "purchase_date": fields.DateTime,
    "product_id": fields.Integer,
    "quantity": fields.Integer,
    "product": fields.Nested({
        "name": fields.String,
        "price": fields.Float,
    })

}


class PurchaseAPI(Resource):
    
    @auth_required('token')
    @roles_accepted('user')
    @marshal_with(purchase_fields)
    # @cache.cached(timeout = 40)
    def get(self):
        order_id = request.args.get("order_id")
        filters_provided = {}
        filters_provided["user_id"] = current_user.id

        if order_id:
            filters_provided["order_id"] = order_id
        purchases = Purchase.query.filter_by(**filters_provided).order_by(Purchase.purchase_date.desc()).all()
        return purchases
    
    
    @auth_required('token')
    @roles_accepted('user')
    def post(self):
        user_id = current_user.id
        cart_products = ShoppingCart.query.filter_by(user_id=user_id).all()
        print(cart_products)
        if not cart_products:
            raise NotFoundError(
                status_code=404,
                error_code="PURCHASE002",
                message="Cart not found or empty",
            )
        order_id = uuid4().hex
        purchase_date = datetime.now()
        for cart_product in cart_products:
            product = cart_product.product
            purchase = Purchase(user_id=user_id, order_id=order_id, product_id=product.id, quantity=cart_product.quantity, purchase_date=purchase_date)
            product.stock -= cart_product.quantity
            db.session.add(purchase)
            db.session.delete(cart_product)
        db.session.commit()
        return jsonify({"message": "Purchase created successfully!!", "order_id": order_id})
    
    
    def delete(self, id):
        purchases = Purchase.query.filter_by(order_id=id).all()
        if purchases:
            for purchase in purchases:
                db.session.delete(purchase)
            db.session.commit()
            return {"message":"Purchase deleted successfully!!"}
        else:
            raise NotFoundError(status_code=404)