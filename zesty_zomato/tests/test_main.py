import unittest
from app.main import app, menu


class TestZestyZomatoApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_homepage(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_create_menu_valid(self):
        response = self.app.post(
            "/menu", json={'dishId': 1, 'dish_name': "Pizza", 'price': 10.33, 'availability': True})
        self.assertEqual(response.status_code, 200)

    def test_create_menu_invalid(self):

        response = self.app.post(
            "/menu", json={"dish_name": "Invalid Dish"}
        )
        self.assertEqual(response.status_code, 400)

    def test_update_menu_valid(self):
        self.app.post(
            "/menu", json={'dishId': 1, 'dish_name': "Pizza", 'price': 10.33, 'availability': True})
        response = self.app.put(
            "/menu/1", json={'dish_name': "New Pizza", 'price': 11.23, 'availability': False}
        )
        self.assertEqual(response.status_code, 200)

        updated_item = menu[0]
        self.assertEqual(updated_item["dish_name"], "New Pizza")
        self.assertEqual(updated_item["price"], 11.23)
        self.assertEqual(updated_item["availability"], False)

    def test_update_invalid_menu_item(self):
        response = self.app.put("/menu/2", json={'dish_name': 'Updated Dish'})
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
