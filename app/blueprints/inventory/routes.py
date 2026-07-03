from .schemas import inventory_schema, inventories_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import db, Inventory, service_ticket
from . import inventories_bp
from app.extensions import limiter, cache
from app.utils.util import encode_token, token_required
from app.blueprints.service_tickets.schemas import service_tickets_schema


@inventories_bp.route('', methods=['POST'])
def create_inventory():
    try:
        inventory_data = inventory_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(Inventory).where(Inventory.name == inventory_data['name'])
    
    existing_inventory = db.session.execute(query).scalars().all()
    if existing_inventory:
        return jsonify({'message': 'Inventory item with this name already exists'}), 400
    
    new_inventory = Inventory(**inventory_data)
    db.session.add(new_inventory)
    db.session.commit()
    return inventory_schema.jsonify(new_inventory), 201


# get all inventory
@inventories_bp.route('', methods=['GET'])
def get_inventories():
    query = select(Inventory)
    inventories = db.session.execute(query).scalars().all()
    return inventories_schema.jsonify(inventories), 200

# get inventory by id
@inventories_bp.route('/<int:inventory_id>', methods=['GET'])
def get_inventory(inventory_id):
    inventory = db.session.get(Inventory, inventory_id)
    if inventory:
        return inventory_schema.jsonify(inventory), 200
    return jsonify({'message': 'inventory not found'}), 404

# update inventory by id
@inventories_bp.route('/<int:inventory_id>', methods=['PUT'])
def update_inventory(inventory_id):
    inventory = db.session.get(Inventory, inventory_id)
    if not inventory:
        return jsonify({'message': 'inventory not found'}), 404
    try:
        inventory_data = inventory_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    for key, value in inventory_data.items():
        setattr(inventory, key, value)
    db.session.commit()
    return inventory_schema.jsonify(inventory), 200

# delete inventory by id
@inventories_bp.route('/<int:inventory_id>', methods=['DELETE'])
def delete_inventory(inventory_id):
    inventory = db.session.get(Inventory, inventory_id)
    if not inventory:
        return jsonify({'message': 'inventory not found'}), 404
    db.session.delete(inventory)
    db.session.commit()
    return jsonify({'message': f'inventory: {inventory_id} deleted successfully'}), 200