from app.extensions import ma
from app.models import service_ticket

class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = service_ticket
        include_fk = True
        
service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)