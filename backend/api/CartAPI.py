from flask import request
from flask_restful import Resource, fields, marshal_with, reqparse
from flask_security import current_user
from flask_security import roles_accepted,auth_required
from application.db import Product, ShoppingCart
from application.db import db
from application.validation import NotFoundError, NotGivenError, SchemaValidationError, PropertyExistError, BusinessValidationError


cart_fields =  {
    "id": fields.Integer,
    "product": fields.Nested({
        "id": fields.Integer,
        "name": fields.String,
        "description": fields.String,
        "price": fields.Float,
        "section_id": fields.Integer,
        "unit": fields.String,
        "stock": fields.Integer,
        "created_at": fields.DateTime,
        "expired_at": fields.DateTime,
    }),
    "quantity": fields.Integer,
}

cart_parse = reqparse.RequestParser()
cart_parse.add_argument("product_id", type=int, required=True, help="Product id is required")
cart_parse.add_argument("quantity", type=int, required=True, help="Product quantity is required")

def validate_product_and_quantity(quantity, product_id):
    if quantity <= 0:
                raise NotGivenError(
                    status_code=400,
                    error_code="CART005",
                    message="Product quantity should be greater than 0",
                )

    prod = Product.query.filter_by(id=product_id).first()

    if prod is None:
        raise NotFoundError(status_code=404, message="Product not found")

    if quantity > prod.stock:
        raise NotGivenError(
            status_code=400,
            error_code="CART006",
            message="Product quantity should be less than or equal to stock",
        )

class CartAPI(Resource):
    @auth_required('token')
    @roles_accepted('user')
    @marshal_with(cart_fields)
    def get(self):
        carts = ShoppingCart.query.filter_by(user_id=current_user.id).all()
        return carts
    

    @auth_required('token')
    @roles_accepted('user')
    def post(self):
        args = cart_parse.parse_args()
        user_id = current_user.id
        product_id = args.get("product_id")
        quantity = args.get("quantity")

        validate_product_and_quantity(quantity, product_id)


        existing_cart_item = ShoppingCart.query.filter_by(user_id=user_id, product_id=product_id).first()
        if existing_cart_item is not None:
            raise PropertyExistError(
                status_code=400,
                message="Product Id-{0} already exists in the cart".format(product_id),
            )

        cart = ShoppingCart(user_id=user_id, product_id=product_id, quantity=quantity)
        db.session.add(cart)

        db.session.commit()
        return {"message": "Added product to cart"}
 

    @auth_required('token')
    @roles_accepted('user')
    def put(self, id):
        args = cart_parse.parse_args()
        product_id = args.get("product_id")
        quantity = args.get("quantity")

        validate_product_and_quantity(quantity, product_id)

        cart = ShoppingCart.query.filter_by(id=id).first()
        if not cart:
            raise NotFoundError(status_code=404, message="Cart not found")
        
        if cart.user_id != current_user.id:
            raise BusinessValidationError(status_code=400, error_code="CART008", message="You are not authorized to update this cart")
        
        cart.quantity = quantity
        db.session.commit()
        return {"message": "Cart updated successfully!!"}
        
        
    @auth_required('token')
    @roles_accepted('user')
    def delete(self, id):
        cart = ShoppingCart.query.filter_by(id=id).first()
        if not cart:
            raise NotFoundError(status_code=404, message="Cart not found")
        if cart.user_id != current_user.id:
            raise BusinessValidationError(status_code=400, error_code="CART008", message="You are not authorized to delete this cart")
        
        db.session.delete(cart)
        db.session.commit()
        return {"message": "Cart deleted successfully!!"}

    