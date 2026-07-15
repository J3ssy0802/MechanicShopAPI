from app import create_app
from app.models import Mechanic, db
import unittest

class TestMechanic(unittest.TestCase):
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

    def test_mechanic_creation(self):
        mechanic_payload = {
            "name": "Jane Doe",
            "email": "jane.doe@example.com",
            "phone": "123-456-7890",
            "salary": 50000
        }

        response = self.client.post('/mechanics', json=mechanic_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "Jane Doe")

    def test_invalid_mechanic_creation(self):
        mechanic_payload = {
            "name": "Jane Doe",
            "phone": "123-456-7890",
            "salary": 50000
        }

        response = self.client.post('/mechanics', json=mechanic_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['email'], ['Missing data for required field.'])

    def test_get_mechanics(self):
        response = self.client.get('/mechanics')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_get_mechanics_by_ticket_count(self):
        response = self.client.get('/mechanics/most-tickets')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_get_mechanic_by_id(self):
        mechanic_payload = {
            "name": "Jane Doe",
            "email": "jane.doe@example.com",
            "phone": "123-456-7890",
            "salary": 50000
        }

        create_response = self.client.post('/mechanics', json=mechanic_payload)
        self.assertEqual(create_response.status_code, 201)

        response = self.client.get('/mechanics/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], "Jane Doe")

    def test_update_mechanic(self):
        mechanic_payload = {
            "name": "Jane Doe",
            "email": "jane.doe@example.com",
            "phone": "123-456-7890",
            "salary": 50000
        }

        create_response = self.client.post('/mechanics', json=mechanic_payload)
        self.assertEqual(create_response.status_code, 201)

        update_payload = {
            "name": "Jane Smith",
            "email": "jane.smith@example.com",
            "phone": "987-654-3210",
            "salary": 60000
        }

        update_response = self.client.put('/mechanics/1', json=update_payload)
        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(update_response.json['name'], "Jane Smith")
        self.assertEqual(update_response.json['email'], "jane.smith@example.com")
        self.assertEqual(update_response.json['phone'], "987-654-3210")
        self.assertEqual(update_response.json['salary'], 60000)

    def test_delete_mechanic(self):
        mechanic_payload = {
            "name": "Jane Doe",
            "email": "jane.doe@example.com",
            "phone": "123-456-7890",
            "salary": 50000
        }

        create_response = self.client.post('/mechanics', json=mechanic_payload)
        self.assertEqual(create_response.status_code, 201)

        response = self.client.delete('/mechanics/1')
        self.assertEqual(response.status_code, 200)