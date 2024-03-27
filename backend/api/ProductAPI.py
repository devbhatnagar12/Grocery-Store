from flask_restful import Resource, fields, marshal_with, reqparse
from flask_security import current_user
from flask_security import roles_accepted,auth_required
from flask import request
from application.db import Product, Section
from application.db import db
from application.validation import NotFoundError, NotGivenError, SchemaValidationError, PropertyExistError, BusinessValidationError
from datetime import datetime


product_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "description": fields.String,
    "price": fields.Float,
    "section_id": fields.Integer,
    "seller_id": fields.Integer,
    "unit": fields.String,
    "stock": fields.Integer,
    "created_at": fields.DateTime,
    "expired_at": fields.DateTime,
    "section": fields.Nested({
        "id": fields.Integer,
        "name": fields.String,
    })
}

product_parse = reqparse.RequestParser()
product_parse.add_argument("name")
product_parse.add_argument("description")
product_parse.add_argument("price")
product_parse.add_argument("section_id")
product_parse.add_argument("seller_id")
product_parse.add_argument("unit")
product_parse.add_argument("stock")
product_parse.add_argument("expired_at")

def parse_args(args):
    arg_errors = {
        "name": "Product name not given",
        "description": "Product description not given",
        "price": "Product price not given",
        "section_id": "Product section not given",
        "unit": "Product unit not given",
        "stock": "Product stock not given",
        "expired_at": "Product expired_at not given",
    }

    for arg, error_message in arg_errors.items():
        if args.get(arg) is None:
            raise NotGivenError(
                status_code=400,
                error_code=f"PRODUCT00{list(arg_errors.keys()).index(arg)+1}",
                message=error_message,
            )

    args["expired_at"] = datetime.strptime(args["expired_at"], '%Y-%m-%d')
    
    return args

def check_product_exists(name, seller_id):
    product = Product.query.filter_by(name=name, seller_id=seller_id).first()
    if product:
        raise PropertyExistError(
            status_code=409,
            message="Product already exists",
        )

def check_section_exists_and_active(section_id):
    section = Section.query.filter_by(id=section_id).first()
    if not section:
        raise NotFoundError(status_code=404, message="Section not found")
    if not section.active:
        raise BusinessValidationError(status_code=400, error_code="SECTION002", message="You are not authorized to create products. Section is not active")

def check_manager_active():
    if not current_user.active:
        raise BusinessValidationError(status_code=400, error_code="USER002", message="You are not authorized to create products. Your account is not active")

class ProductAPI(Resource):
    @auth_required('token')
    @marshal_with(product_fields)
    def get(self):
        """
        Retrieves the products based on the provided filters.

        Parameters:
        - seller_only (str): If set to 'True', retrieves products belonging to the current user only.
        - section_id (str): The ID of the section to filter the products.

        Returns:
        - list: A list of products that match the provided filters. If no filters are provided, returns all products.
        """
        seller_id = request.args.get("seller_only")
        section_id = request.args.get("section_id")  
        product_id = request.args.get("product_id")       
        filters_provided = {}
        print(seller_id, section_id)
        if seller_id == "true":
            filters_provided["seller_id"] = current_user.id
        if section_id:
            filters_provided["section_id"] = section_id
        if product_id:
            filters_provided["id"] = product_id
        if filters_provided:
            products = Product.query.filter_by(**filters_provided).all()
            return products
        
        products = Product.query.all()
        return products
    
    @auth_required('token')
    @roles_accepted('manager')
    @marshal_with(product_fields)
    def put(self, product_id):
        args = product_parse.parse_args()
        args = parse_args(args)
        
        check_manager_active()
        check_section_exists_and_active(args["section_id"])
        
        product = Product.query.filter_by(id=product_id).first()
        if not product: 
            raise NotFoundError(status_code=404, message="Product not found")

        product.name = args["name"]
        product.description = args["description"]
        product.price = args["price"]
        product.section_id = args["section_id"]
        product.unit = args["unit"]
        product.stock = args["stock"]
        product.expired_at = args["expired_at"]
        db.session.commit()
        
        return product

    @auth_required('token')
    @roles_accepted('manager')
    @marshal_with(product_fields)
    def post(self):
        args = product_parse.parse_args()
        args = parse_args(args)

        check_manager_active()
        check_section_exists_and_active(args["section_id"])

        product = Product.query.filter_by(name=args["name"], seller_id=current_user.id, section_id=args["section_id"], price=args["price"], description=args["description"]).first()
        if product:
            raise PropertyExistError(
                status_code=409,
                message="Product already exists",
            )
        

        product = Product(**args)
        product.seller_id = current_user.id
        
        db.session.add(product)
        db.session.commit()
        return product
    
    @auth_required('token')
    @roles_accepted('manager')
    def delete(self, product_id):
        product = Product.query.filter_by(id=product_id).first()
        print(product.seller_id, current_user.id)
        if product.seller_id != current_user.id:
            raise BusinessValidationError(status_code=400, error_code="PRODUCT001", message="You are not authorized to delete this product. You can only delete products for your own section")
        if not product:
            raise NotFoundError(status_code=404, message="Product not found")

        db.session.delete(product)
        db.session.commit()
        return {"message":"Product deleted successfully"}
            
    