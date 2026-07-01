from .schemas import service_ticket_schema, service_tickets_schema, edit_service_ticket_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import db, service_ticket, Mechanic
from . import service_tickets_bp


#create a new service ticket
@service_tickets_bp.route('', methods=['POST'])
def create_service_ticket():
    try:
        service_ticket_data = service_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_service_ticket = service_ticket(**service_ticket_data)
    db.session.add(new_service_ticket)
    db.session.commit()
    return service_ticket_schema.jsonify(new_service_ticket), 201

#assign a mechanic to a service ticket
@service_tickets_bp.route('/<int:ticket_id>/assign_mechanic/<int:mechanic_id>', methods=['PUT'])
def assign_mechanic(ticket_id, mechanic_id):
    ticket = db.session.get(service_ticket, ticket_id)
    if not ticket:
        return jsonify({'message': 'Service ticket not found'}), 404

    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return jsonify({'message': 'Mechanic not found'}), 404
    
    if mechanic in ticket.mechanics:
        return jsonify({'message': 'Mechanic already assigned to this ticket'}), 200

    ticket.mechanics.append(mechanic)
    db.session.commit()
    return service_ticket_schema.jsonify(ticket), 200

#update mechanics assigned to a service ticket
@service_tickets_bp.route('/<int:ticket_id>/update_mechanics', methods=['PUT'])
def update_mechanic(ticket_id):
    try:
        service_ticket_edit = edit_service_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(service_ticket).where(service_ticket.id == ticket_id)
    ticket = db.session.execute(query).scalars().first()

    for mechanic_id in service_ticket_edit['add_mechanic_id']:
        query = select(Mechanic).where(Mechanic.id == mechanic_id)
        mechanic = db.session.execute(query).scalars().first()

        if mechanic and mechanic not in ticket.mechanics:
            ticket.mechanics.append(mechanic)

    for mechanic_id in service_ticket_edit['remove_mechanic_id']:
        query = select(Mechanic).where(Mechanic.id == mechanic_id)
        mechanic = db.session.execute(query).scalars().first()

        if mechanic and mechanic in ticket.mechanics:
            ticket.mechanics.remove(mechanic)

    db.session.commit()
    return service_ticket_schema.jsonify(ticket), 200


#get all service tickets
@service_tickets_bp.route('', methods=['GET'])
def get_all_service_tickets():
    tickets = db.session.execute(select(service_ticket)).scalars().all()
    return service_tickets_schema.jsonify(tickets), 200