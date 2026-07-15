from app import create_app
from app.models import db, Customer
from app.utils.util import encode_token
import unittest

class TestCustomer(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig")
        self.customer = Customer(name="test_user", email="test@email.com", password="test")
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.customer)
            db.session.commit()
        self.token = encode_token(1)
        self.client = self.app.test_client()

    def tearDown(self):
        with self.app.app_context():
            db.session.close()
            db.session.remove()
            db.drop_all()
            db.engine.dispose()

    def _login_and_get_token(self):
        credentials = {
            "email": "test@email.com",
            "password": "test"
        }

        response = self.client.post('/customers/login', json=credentials)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'success')
        return response.json['token']

    def test_create_customer(self):
        customer_payload = {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "password": "password123"
        }

        response = self.client.post('/customers', json=customer_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "John Doe")

    def test_invalid_creation(self):
        customer_payload = {
            "name": "John Doe",
            "password": "password123"
        }

        response = self.client.post('/customers', json=customer_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['email'], ['Missing data for required field.'])

    def test_login_customer(self):
        self._login_and_get_token()
    
    def test_invalid_login(self):
        credentials = {
            "email": "bad_email@email.com",
            "password": "bad_pw"
        }

        response = self.client.post('/customers/login', json=credentials)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json['message'], 'Invalid email or password')

    def test_update_customer(self):
        update_payload = {
            "name": "Updated Name"
        }

        headers = {'Authorization': "Bearer " + self._login_and_get_token()}

        response = self.client.put('/customers/', json=update_payload, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], "Updated Name")
        self.assertEqual(response.json['email'], "test@email.com")

    def test_get_all_customers(self):
        response = self.client.get('/customers')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]['name'], 'test_user')

    def test_get_customer_by_id(self):
        response = self.client.get('/customers/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'test_user')

    def test_delete_customer(self):
        headers = {'Authorization': "Bearer " + self._login_and_get_token()}

        response = self.client.delete('/customers/', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Customer: 1 deleted successfully')

    def test_get_service_tickets_for_customer(self):
        headers = {'Authorization': "Bearer " + self._login_and_get_token()}
        # Create a service ticket for the customer
        service_ticket_payload = {
            "customer_id": 1,
            "VIN": "1HGCM82633A004352",
            "service_date": "2024-06-01",
            "service_description": "Oil change and tire rotation"
        }
        response = self.client.post('/service_tickets', json=service_ticket_payload)
        self.assertEqual(response.status_code, 201)

        # Get service tickets for the customer
        response = self.client.get('/customers/my-tickets', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        self.assertEqual(response.json[0]['VIN'], "1HGCM82633A004352")
