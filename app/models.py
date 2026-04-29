from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column



class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class= Base)


service_ticket_mechanic = db.Table(
    'service_ticket_mechanic',
    db.Column('service_ticket_id', db.Integer, db.ForeignKey('service_tickets.id'), primary_key=True),
    db.Column('mechanic_id', db.Integer, db.ForeignKey('mechanics.id'), primary_key=True)
)

class Customer(Base):
    __tablename__ = 'customers'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(255), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(db.String(255), nullable=False)
    
    service_tickets: Mapped[list["service_ticket"]] = db.relationship(back_populates='customer')
    
class service_ticket(Base):
    __tablename__ = 'service_tickets'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(db.ForeignKey('customers.id'), nullable=False)
    VIN: Mapped[str] = mapped_column(db.String(255), nullable=False)
    service_date: Mapped[str] = mapped_column(db.String(255), nullable=False)
    service_description: Mapped[str] = mapped_column(db.String(255), nullable=False)
    
    customer: Mapped[Customer] = db.relationship(back_populates='service_tickets')
    mechanics: Mapped[list["Mechanic"]] = db.relationship(secondary=service_ticket_mechanic, back_populates='service_tickets')
    
class Mechanic(Base):
    __tablename__ = 'mechanics'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(255), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(db.String(255), nullable=False)
    salary: Mapped[float] = mapped_column(db.Float, nullable=False)
    
    service_tickets: Mapped[list[service_ticket]] = db.relationship(secondary=service_ticket_mechanic, back_populates='mechanics')
