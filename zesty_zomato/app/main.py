from flask import Flask, request, jsonify
app = Flask(__name__)

menu = [
    {
        "dishId": 1,
        "dish_name": "Spaghetti Carbonara",
        "price": 12.99,
        "availability": True
    },
    {
        "dishId": 2,
        "dish_name": "Margherita Pizza",
        "price": 10.49,
        "availability": True
    },
    {
        "dishId": 3,
        "dish_name": "Chicken Alfredo",
        "price": 14.99,
        "availability": True
    },
    {
        "dishId": 4,
        "dish_name": "Caesar Salad",
        "price": 8.99,
        "availability": True
    },
    {
        "dishId": 5,
        "dish_name": "Hamburger",
        "price": 9.99,
        "availability": True
    },
    {
        "dishId": 6,
        "dish_name": "Sushi Platter",
        "price": 22.99,
        "availability": True
    },
    {
        "dishId": 7,
        "dish_name": "Veggie Wrap",
        "price": 7.99,
        "availability": True
    },
    {
        "dishId": 8,
        "dish_name": "Chocolate Cake",
        "price": 6.49,
        "availability": True
    },
    {
        "dishId": 9,
        "dish_name": "Grilled Salmon",
        "price": 16.99,
        "availability": True
    },
    {
        "dishId": 10,
        "dish_name": "Fruit Salad",
        "price": 5.99,
        "availability": True
    }
]


orders = []
orderCounter = 1


@app.route("/")
def homepage():
    return jsonify(menu_data=menu), 200


@app.route("/menu", methods=["POST"])
def create_menu():
    data = request.json
    if "dishId" not in data or "dish_name" not in data or "price" not in data:
        return jsonify({"error": "Invalid JSON Data"}), 400
    menu.append(data)
    return jsonify({'message': 'Menu item created'}), 201


@app.route("/menu/<int:dishId>", methods=["PUT"])
def update_menu(dishId):
    data = request.json
    for item in menu:
        if item["dishId"] == dishId:
            item.update(data)
            return jsonify({'message': "Menu Updated"}), 200
    return jsonify({'error': 'Menu item not found'}), 404


@app.route("/menu/<int:dishId>", methods=["DELETE"])
def delete_menu(dishId):
    for item in menu:
        if item["dishId"] == dishId:
            menu.remove(item)
            return jsonify({"message": "Item Deleted"}), 204
    return jsonify({"error": "Item not found"}), 404


@app.route("/orders", methods=["POST"])
def order_placed():
    data = request.json
    customer_name = data.get("customer_name")
    dish_ids = data.get("dish_ids")

    if not customer_name or not dish_ids:
        return jsonify({"message": "Invalid Order"}), 400
    
    if len(set(dish_ids)) != len(dish_ids):
        return jsonify({"error": "Duplicate dish_ids are not allowed in a single order"}), 400

    orderItems = []
    totalPrice = 0

    for id in dish_ids:
        dish = next((item for item in menu if item["dishId"] == id), None)
        if dish and dish["availability"]:
            orderItems.append(dish)
            totalPrice += dish["price"]
        else:
            return jsonify({"error": f"Dish with dishId {id} is unavailabile"}), 400

    global orderCounter
    order_id = orderCounter
    orderCounter += 1

    order = {
        "order_id": order_id,
        "customer_name": customer_name,
        "order_items": orderItems,
        "total_price": totalPrice,
        "order_status": "received"
    }

    orders.append(order)
    return jsonify({"message": f"Order with order_id {order_id} placed successfully"}), 201

@app.route("/orders", methods=["GET"])
def get_orders():
    status_filter = request.args.get("status")
    if status_filter:
        filtered_orders = [order for order in orders if order["order_status"] == status_filter]
    else:
        filtered_orders = orders
    return jsonify(filtered_orders), 200

@app.route("/orders/<int:order_id>", methods=["PUT"])
def update_order_status(order_id):
    new_status = request.json.get("order_status")
    
    for order in orders:
        if order["order_id"] == order_id:
            if new_status in ["Preparing", "Ready to pickup", "Delivered"]:
                order["order_status"] = new_status
                return jsonify({"message": f"Order {order_id} status updated to {new_status}"}), 200
            else:
                return jsonify({"error": "Invalid order_status"}), 400
    
    return jsonify({"error": f"Order with order_id {order_id} not found"}), 404






if __name__ == '__main__':
    app.run()
