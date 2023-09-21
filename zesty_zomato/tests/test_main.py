import unittest
from app.main import app, menu


class TestZestyZomatoApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

# test for get

    def test_display_menu(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

        response_data = response.get_json()
        self.assertIn('menu_data', response_data)

# test for get

# Tests for post

    def test_create_menu_valid(self):
        response = self.app.post(
            "/menu", json={'dishId': 1, 'dish_name': "Pizza", 'price': 10.33, 'availability': True})
        self.assertEqual(response.status_code, 201)

    def test_create_menu_invalid(self):

        response = self.app.post(
            "/menu", json={"dish_name": "Invalid Dish"}
        )
        self.assertEqual(response.status_code, 400)

# Tests for post

# Tests for update

    def test_update_menu_valid(self):
        self.app.post(
            "/menu", json={'dishId': 11, 'dish_name': "Pizza", 'price': 10.33, 'availability': True})
        response = self.app.put(
            "/menu/11", json={'dish_name': "New Pizza", 'price': 11.23, 'availability': False}
        )
        self.assertEqual(response.status_code, 200)

        updated_item = next(item for item in menu if item["dishId"] == 11)
        self.assertEqual(updated_item["dish_name"], "New Pizza")
        self.assertEqual(updated_item["price"], 11.23)
        self.assertEqual(updated_item["availability"], False)

    def test_update_invalid_menu_item(self):
        response = self.app.put("/menu/99", json={'dish_name': 'Updated Dish'})
        self.assertEqual(response.status_code, 404)

# Tests for update

# Tests for delete

    def test_delete_menu_item(self):
        self.app.post(
            "/menu", json={'dishId': 11, 'dish_name': "Pizza", 'price': 10.33, 'availability': True}
        )
        response = self.app.delete(
            "/menu/11"
        )
        self.assertEqual(response.status_code, 204)

    def test_delete_invalid_item(self):
        response = self.app.delete("menu/99")
        self.assertEqual(response.status_code, 404)

# Tests for delete

# Tests for  Order Placed

    def test_order_placed(self):
        response = self.app.post(
            "/orders",
            json={"customer_name": "Ansh", "dish_ids": [1, 2, 3]}
        )
        self.assertEqual(response.status_code, 201)

    def test_order_placed_failed(self):
        response = self.app.post(
            "/orders",
            json={"customer_name": "Ansh", "dish_ids": [12, 13, 14]}
        )
        self.assertEqual(response.status_code, 400)

# Tests for  Order Placed

# Tests for  Update Placed

    def test_order_update(self):
        response = self.app.post(
            "/orders",
            json={"customer_name": "Ansh", "dish_ids": [1, 2, 3]}
        )

        orderId = response.get_json().get("message").split()[-1]
        response = self.app.put(
            f"/orders/{orderId}",
            json={"order_status": "prepared"}
        )
        self.assertEqual(response.status_code, 200)


# Tests for  Update Placed


if __name__ == '__main__':
    unittest.main()
