from flask import Flask, request, jsonify
app = Flask(__name__)

menu = []

@app.route("/")
def homepage():
    return 'Welcome to Zesty Zomato!', 200

@app.route("/menu", methods=["POST"])
def create_menu():
    data = request.json
    if "dishId" not in data or "dish_name" not in data or "price" not in data:
        return jsonify({"error": "Invalid JSON Data"}), 400
    menu.append(data)
    return jsonify({'message': 'Menu item created'}), 200

@app.route("/menu/<int:dishId>", methods=["PUT"])
def update_menu(dishId):
    data = request.json
    for item in menu:
        if item["dishId"] == dishId:
            item.update(data)
            return jsonify({'message' : "Menu Updated"}), 200
    return jsonify({'error': 'Menu item not found'}), 404


if __name__ == '__main__':
    app.run()


