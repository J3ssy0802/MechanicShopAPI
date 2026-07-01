from app.extensions import ma
from app.models import service_ticket
from marshmallow import fields

class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    customer = fields.Nested('CustomerSchema', only=['id', 'name'])
    mechanics = fields.Nested('MechanicSchema', many=True, only=['id', 'name'])
    class Meta:
        model = service_ticket
        include_fk = True
        fields = ('id', 'customer_id', 'VIN', 'service_date', 'service_description', 'customer', 'mechanics')

class EditServiceTicketSchema(ma.Schema):
        add_mechanic_id = fields.List(fields.Int(), required=True)
        remove_mechanic_id = fields.List(fields.Int(), required=True)
        class Meta:
            fields = ('add_mechanic_id', 'remove_mechanic_id')
        
service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)
edit_service_ticket_schema = EditServiceTicketSchema()