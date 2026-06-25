from .schemas import customer_schema, customers_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import db, Customer, service_ticket
from . import customers_bp
from app.extensions import limiter, cache
from app.utils.util import encode_token, token_required
from app.blueprints.service_tickets.schemas import service_tickets_schema

# create a new customer
@customers_bp.route('', methods=['POST'])
@limiter.limit("10 per hour") # limit to 10 requests per hour for this endpoint to prevent abuse
def create_customer():
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(Customer).where(Customer.email == customer_data['email'])
    
    existing_customer = db.session.execute(query).scalars().all()
    if existing_customer:
        return jsonify({'message': 'Customer with this email already exists'}), 400
    
    new_customer = Customer(**customer_data)
    db.session.add(new_customer)
    db.session.commit()
    return customer_schema.jsonify(new_customer), 201

# get all customers
@customers_bp.route('', methods=['GET'])
@cache.cached(timeout=120) # cache the response for 120 seconds to improve performance due to potentially expensive database query for repetitive requests
def get_customers():
    query = select(Customer)
    customers = db.session.execute(query).scalars().all()
    return customers_schema.jsonify(customers), 200
    
# get customer by id
@customers_bp.route('/<int:customer_id>', methods=['GET'])
@limiter.limit("10 per hour") # limit to 10 requests per hour for this endpoint to prevent abuse
def get_customer(customer_id):
    customer = db.session.get(Customer, customer_id)
    if customer:
        return customer_schema.jsonify(customer), 200
    return jsonify({'message': 'Customer not found'}), 404

# update customer by id  
@customers_bp.route('/<int:customer_id>', methods=['PUT'])
@token_required
def update_customer(customer_id):
    customer = db.session.get(Customer, customer_id)
    if not customer:
        return jsonify({'message': 'Customer not found'}), 404
    
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for key, value in customer_data.items():
        setattr(customer, key, value)
    
    db.session.commit()
    return customer_schema.jsonify(customer), 200

#customer login
@customers_bp.route('/login', methods=['POST'])
def login():
    try:
        credentials = request.json
        username = credentials['email']
        password = credentials['password']
    except KeyError:
        return jsonify({'message': 'Invalid payload, expecting username and password'}), 400
    
    query = select(Customer).where(Customer.email == username)
    customer = db.session.execute(query).scalar_one_or_none()

    if customer and customer.password == password:
        auth_token = encode_token(customer.id, customer.role.role_name)

        response = {
            "status": "success",
            "message": "Successfully logged in.",
            "auth_token": auth_token
        }
        return jsonify(response), 200
    else:
        return jsonify({'message': 'Invalid email or password'}), 401
    
#delete customer by id with token authentication
@customers_bp.route('/', methods=['DELETE'])
@token_required
def delete_customer(customer_id):
    query = select(Customer).where(Customer.id == customer_id)
    customer = db.session.execute(query).scalars().first()

    db.session.delete(customer)
    db.session.commit()
    return jsonify({'message': f'Customer: {customer_id} deleted successfully'}), 200


# get all service tickets for the authenticated customer
@customers_bp.route('/my-tickets', methods=['GET'])
@token_required
def get_my_tickets(customer_id):
    try:
        customer_id = int(customer_id)
    except (TypeError, ValueError):
        return jsonify({'message': 'Token is invalid!'}), 401

    query = select(service_ticket).where(service_ticket.customer_id == customer_id)
    tickets = db.session.execute(query).scalars().all()
    return service_tickets_schema.jsonify(tickets), 200
    

