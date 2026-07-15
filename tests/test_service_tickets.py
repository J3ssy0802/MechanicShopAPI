from app import create_app
from app.models import db
import unittest

class TestServiceTickets(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig")
        with self.app.app_context():
            db.drop_all()
            db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        with self.app.app_context():
            db.session.close()
            db.session.remove()
            db.drop_all()
            db.engine.dispose()

    def test_service_ticket_creation(self):
        service_ticket_payload = {
            "customer_id": 1,
            "VIN": "1HGCM82633A004352",
            "service_date": "2024-06-01",
            "service_description": "Oil change and tire rotation"
        }

        response = self.client.post('/service_tickets', json=service_ticket_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['VIN'], "1HGCM82633A004352")

    def test_invalid_service_ticket_creation(self):
        service_ticket_payload = {
            "customer_id": 1,
            "service_date": "2024-06-01",
            "service_description": "Oil change and tire rotation"
        }

        response = self.client.post('/service_tickets', json=service_ticket_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['VIN'], ['Missing data for required field.'])

    def test_get_service_tickets(self):
        response = self.client.get('/service_tickets')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_assign_mechanic_to_service_ticket(self):
        # Create a service ticket
        service_ticket_payload = {
            "customer_id": 1,
            "VIN": "1HGCM82633A004352",
            "service_date": "2024-06-01",
            "service_description": "Oil change and tire rotation"
        }
        response = self.client.post('/service_tickets', json=service_ticket_payload)
        self.assertEqual(response.status_code, 201)
        ticket_id = response.json['id']

        # Create a mechanic
        mechanic_payload = {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "phone": "123-456-7890",
            "salary": 50000
        }
        response = self.client.post('/mechanics', json=mechanic_payload)
        self.assertEqual(response.status_code, 201)
        mechanic_id = response.json['id']

        # Assign the mechanic to the service ticket
        response = self.client.put(f'/service_tickets/{ticket_id}/assign_mechanic/{mechanic_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(mechanic_id, [m['id'] for m in response.json['mechanics']])

    def test_update_mechanics_assigned_to_service_ticket(self):
        # Create a service ticket
        service_ticket_payload = {
            "customer_id": 1,
            "VIN": "1HGCM82633A004352",
            "service_date": "2024-06-01",
            "service_description": "Oil change and tire rotation"
        }
        response = self.client.post('/service_tickets', json=service_ticket_payload)
        self.assertEqual(response.status_code, 201)
        ticket_id = response.json['id']

        # Create two mechanics
        mechanic_payload_1 = {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "phone": "123-456-7890",
            "salary": 50000
        }
        response = self.client.post('/mechanics', json=mechanic_payload_1)
        self.assertEqual(response.status_code, 201)
        mechanic_id_1 = response.json['id']

        mechanic_payload_2 = {
            "name": "Jane Smith",
            "email": "jane.smith@example.com",
            "phone": "987-654-3210",
            "salary": 55000
        }
        response = self.client.post('/mechanics', json=mechanic_payload_2)
        self.assertEqual(response.status_code, 201)
        mechanic_id_2 = response.json['id']

        # Assign the first mechanic to the service ticket
        response = self.client.put(f'/service_tickets/{ticket_id}/assign_mechanic/{mechanic_id_1}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(mechanic_id_1, [m['id'] for m in response.json['mechanics']])

        # Update the mechanics assigned to the service ticket
        update_payload = {
            "add_mechanic_id": [mechanic_id_2],
            "remove_mechanic_id": [mechanic_id_1]
        }
        response = self.client.put(f'/service_tickets/{ticket_id}/update_mechanics', json=update_payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn(mechanic_id_2, [m['id'] for m in response.json['mechanics']])
        self.assertNotIn(mechanic_id_1, [m['id'] for m in response.json['mechanics']])
        
    def test_assign_inventory_item_to_service_ticket(self):
        # Create a service ticket
        service_ticket_payload = {
            "customer_id": 1,
            "VIN": "1HGCM82633A004352",
            "service_date": "2024-06-01",
            "service_description": "Oil change and tire rotation"
        }
        response = self.client.post('/service_tickets', json=service_ticket_payload)
        self.assertEqual(response.status_code, 201)
        ticket_id = response.json['id']

        # Create an inventory item
        inventory_item_payload = {
            "name": "Oil Filter",
            "price": 15.99
        }
        response = self.client.post('/inventory', json=inventory_item_payload)
        self.assertEqual(response.status_code, 201)
        item_id = response.json['id']

        # Assign the inventory item to the service ticket
        response = self.client.put(f'/service_tickets/{ticket_id}/assign_inventory/{item_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(item_id, [i['id'] for i in response.json['inventory_items']])
