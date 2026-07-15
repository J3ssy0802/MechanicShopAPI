from app import create_app
from app.models import db
import unittest

class TestInventory(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig")
        with self.app.app_context():
            db.drop_all()
            db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_inventory_item(self):
        inventory_item_payload = {
            "name": "Brake Pad",
            "price": 50
        }

        response = self.client.post('/inventory', json=inventory_item_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "Brake Pad")

    def test_get_inventories(self):
        # First, create an inventory item
        inventory_item_payload = {
            "name": "Brake Pad",
            "price": 50
        }
        self.client.post('/inventory', json=inventory_item_payload)

        response = self.client.get('/inventory')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)
        self.assertEqual(response.json[0]['name'], "Brake Pad")

        #Then, create another inventory item
        inventory_item_payload2 = {
            "name": "Oil Filter",
            "price": 20
        }
        self.client.post('/inventory', json=inventory_item_payload2)

        # Finally, get all inventory items and check if both items are present
        response = self.client.get('/inventory')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 2)
        self.assertEqual(response.json[1]['name'], "Oil Filter")

    def test_get_inventory_by_id(self):
        # First, create an inventory item
        inventory_item_payload = {
            "name": "Brake Pad",
            "price": 50
        }
        post_response = self.client.post('/inventory', json=inventory_item_payload)
        inventory_id = post_response.json['id']

        # Then, get the inventory item by ID and check if the correct item is returned
        response = self.client.get(f'/inventory/{inventory_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], "Brake Pad")

    def test_update_inventory_by_id(self):
        # First, create an inventory item
        inventory_item_payload = {
            "name": "Brake Pad",
            "price": 50
        }
        post_response = self.client.post('/inventory', json=inventory_item_payload)
        inventory_id = post_response.json['id']

        # Then, update the inventory item by ID and check if the correct item is updated
        updated_inventory_item_payload = {
            "name": "Brake Pad Pro",
            "price": 70
        }
        response = self.client.put(f'/inventory/{inventory_id}', json=updated_inventory_item_payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], "Brake Pad Pro")
        self.assertEqual(response.json['price'], 70)

    def test_delete_inventory_by_id(self):
        # First, create an inventory item
        inventory_item_payload = {
            "name": "Brake Pad",
            "price": 50
        }
        post_response = self.client.post('/inventory', json=inventory_item_payload)
        inventory_id = post_response.json['id']

        # Then, delete the inventory item by ID and check if the correct item is deleted
        response = self.client.delete(f'/inventory/{inventory_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], f'inventory: {inventory_id} deleted successfully')

        # Finally, try to get the deleted inventory item by ID and check if it returns a 404 status code
        response = self.client.get(f'/inventory/{inventory_id}')
        self.assertEqual(response.status_code, 404)

